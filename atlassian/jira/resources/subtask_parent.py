"""Jira Server's Move Subtask Parent web action (not the sorting REST API)."""

from html.parser import HTMLParser
from urllib.parse import parse_qs, urljoin, urlsplit

import httpx


class SubtaskReparentError(RuntimeError):
    """A rejected or unverified move. Read parent before retrying an unknown result."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class _MoveForm(HTMLParser):
    def __init__(self, html: str, action: str, issue_id: str):
        super().__init__()
        self.active = False
        self.action = ""
        self.fields = {}
        self.feed(html)
        parsed = urlsplit(self.action)
        # Do not forward credentials or CSRF tokens to arbitrary form actions.
        if (
            parsed.scheme
            or parsed.netloc
            or parsed.path != action
            or parse_qs(parsed.query).get("id") != [issue_id]
            or not self.fields.get("atl_token")
        ):
            raise SubtaskReparentError(
                "unsupported_form", "Unexpected Jira move form; use the web UI"
            )

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.active = (
                attrs.get("name") == "jiraform"
                and attrs.get("method", "").lower() == "post"
            )
            if self.active:
                self.action = attrs.get("action", "")
        if self.active and tag == "input" and attrs.get("name"):
            self.fields[attrs["name"]] = attrs.get("value", "")

    def handle_endtag(self, tag):
        if tag == "form":
            self.active = False


def _summary(issue):
    fields = issue["fields"]
    return {
        "id": issue["id"],
        "key": issue["key"],
        "summary": fields["summary"],
        "project": {k: fields["project"][k] for k in ("id", "key")},
        "issue_type": {k: fields["issuetype"][k] for k in ("id", "name", "subtask")},
    }


async def preview_reparent(resource, subtask_key, target_parent_key):
    fields = ["parent", "project", "issuetype", "summary", "subtasks"]
    child = await resource.get_raw(subtask_key, fields=fields)
    target = await resource.get_raw(target_parent_key, fields=fields)
    cf, tf = child["fields"], target["fields"]
    if not cf["issuetype"]["subtask"] or not cf.get("parent"):
        raise ValueError("Source must be an existing subtask with a parent")
    if tf["issuetype"]["subtask"] or child["id"] == target["id"]:
        raise ValueError("Target must be a standard parent issue, not a subtask")
    if cf["project"]["id"] != tf["project"]["id"]:
        raise ValueError("Reparenting requires source and target in the same project")
    source = await resource.get_raw(cf["parent"]["key"], fields=fields)
    info = await resource.client.get_json("/rest/api/2/serverInfo")
    permissions = await resource.client.get_json(
        "/rest/api/2/mypermissions", params={"issueKey": child["key"]}
    )
    permissions = permissions["permissions"]
    can_move = any(
        permissions.get(k, {}).get("havePermission") is True
        for k in ("MOVE_ISSUES", "MOVE_ISSUE")
    )
    supported = (
        info.get("version") == "8.13.5"
        and info.get("deploymentType") == "Server"
        and resource.client.auth_mode == "basic"
        and urlsplit(resource.client.base_url).path in ("", "/")
    )
    return {
        "subtask": _summary(child),
        "source_parent": _summary(source),
        "target_parent": _summary(target),
        "no_change": source["id"] == target["id"],
        "source_subtasks": [x["key"] for x in source["fields"].get("subtasks", [])],
        "target_subtasks": [x["key"] for x in tf.get("subtasks", [])],
        "server_version": info.get("version"),
        "deployment_type": info.get("deploymentType"),
        "auth_mode": resource.client.auth_mode,
        "supported": supported,
        "can_move": can_move,
        "route": "web_move_subtask_parent" if supported else None,
    }


async def _read_result(resource, preview):
    child = await resource.get_raw(preview["subtask"]["key"], fields=["parent"])
    source = await resource.get_raw(
        preview["source_parent"]["key"], fields=["subtasks"]
    )
    target = await resource.get_raw(
        preview["target_parent"]["key"], fields=["subtasks"]
    )
    key = child["key"]
    source_keys = [x["key"] for x in source["fields"].get("subtasks", [])]
    target_keys = [x["key"] for x in target["fields"].get("subtasks", [])]
    parent_id = child["fields"].get("parent", {}).get("id")
    verified = (
        child["id"] == preview["subtask"]["id"]
        and key == preview["subtask"]["key"]
        and parent_id == target["id"]
        and key in target_keys
        and key not in source_keys
    )
    return {
        "verified": verified,
        "parent": child["fields"].get("parent", {}).get("key"),
        "source_subtasks": source_keys,
        "target_subtasks": target_keys,
    }


async def reparent_subtask(resource, subtask_key, target_parent_key):
    preview = await preview_reparent(resource, subtask_key, target_parent_key)
    if preview["no_change"]:
        if preview["subtask"]["key"] not in preview["target_subtasks"]:
            raise SubtaskReparentError(
                "inconsistent_state", "Parent and subtask list disagree"
            )
        return {**preview, "status": "no_change"}
    if not preview["supported"]:
        raise SubtaskReparentError(
            "unsupported_server",
            "Only Jira Server 8.13.5 with Basic authentication is verified; use the web UI",
        )
    if not preview["can_move"]:
        raise SubtaskReparentError(
            "permission_denied", "Move Issues permission is required"
        )
    client = resource.client
    issue_id = preview["subtask"]["id"]
    response = await client.get(
        "/secure/MoveSubTaskChooseOperation!default.jspa",
        params={"id": issue_id},
        follow_redirects=False,
    )
    response.raise_for_status()
    choose = _MoveForm(response.text, "MoveSubTaskChooseOperation.jspa", issue_id)
    if choose.fields.get("operation") != "move.subtask.parent.operation.name":
        raise SubtaskReparentError(
            "unsupported_form", "Change parent operation is unavailable"
        )
    response = await client.post(
        "/secure/" + choose.action,
        data={
            "atl_token": choose.fields["atl_token"],
            "operation": "move.subtask.parent.operation.name",
        },
        follow_redirects=False,
    )
    # The wizard redirects to its parent-selection page; do not forward auth
    # to an arbitrary Location returned by a proxy or a customized instance.
    if response.status_code == 302:
        location = urlsplit(
            urljoin(client.base_url + "/", response.headers.get("location", ""))
        )
        base = urlsplit(client.base_url)
        if (location.scheme, location.netloc) != (
            base.scheme,
            base.netloc,
        ) or location.path != "/secure/MoveSubTaskParent!default.jspa":
            raise SubtaskReparentError(
                "unsupported_form", "Unexpected Jira wizard redirect"
            )
        response = await client.get(
            location.path + ("?" + location.query if location.query else ""),
            follow_redirects=False,
        )
    if response.status_code != 200:
        raise SubtaskReparentError(
            "unsupported_form", "Jira did not return the parent selection form"
        )
    form = _MoveForm(response.text, "MoveSubTaskParent.jspa", issue_id)
    if form.fields.get("id") != issue_id or "parentIssue" not in form.fields:
        raise SubtaskReparentError(
            "unsupported_form", "Unexpected parent selection fields"
        )
    # Recheck immediately before the only parent-changing request.
    child = await resource.get_raw(preview["subtask"]["key"], fields=["parent"])
    if child["fields"].get("parent", {}).get("id") != preview["source_parent"]["id"]:
        raise SubtaskReparentError(
            "concurrent_change", "Parent changed during preparation; preview again"
        )
    status_code = None
    try:
        response = await client.post(
            "/secure/" + form.action,
            data={
                "atl_token": form.fields["atl_token"],
                "id": issue_id,
                "parentIssue": preview["target_parent"]["key"],
            },
            follow_redirects=False,
        )
        status_code = response.status_code
    except httpx.TransportError:
        # The server may already have committed. Never replay this POST.
        pass
    try:
        result = await _read_result(resource, preview)
    except (httpx.HTTPError, KeyError, ValueError):
        raise SubtaskReparentError(
            "result_unknown",
            "Cannot verify move; read parent and both subtask lists before retrying",
        ) from None
    if result["verified"]:
        return {**preview, **result, "status": "moved"}
    if status_code in (400, 401, 403, 404):
        raise SubtaskReparentError(
            "move_rejected", f"Jira rejected the parent change (HTTP {status_code})"
        )
    raise SubtaskReparentError(
        "result_unknown",
        "Parent change was not verified; inspect parent and both subtask lists before retrying",
    )
