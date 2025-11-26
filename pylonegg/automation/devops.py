import base64
import requests
import json
from pylonegg.database import save_task


def read_devops_tasks(
    organization,
    project,
    assigned_to_email,
    token,
    include_fields=None
):
    """
    Fetch unresolved Azure DevOps work items assigned to you.
    Returns a list of dicts similar to Outlook task objects.
    """

    if include_fields is None:
        include_fields = [
            "System.Id",
            "System.Title",
            "System.Description",
            "System.State",
            "System.AssignedTo",
            "System.WorkItemType",
            "Microsoft.VSTS.Scheduling.DueDate",
            "Microsoft.VSTS.Common.Priority"
        ]

    pat_bytes = f":{token}".encode("utf-8")
    pat_token = base64.b64encode(pat_bytes).decode("utf-8")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {token}"
    }

    # WIQL query to get unresolved items assigned to you
    wiql = {
        "query": f"""
        SELECT [System.Id], [System.Title], [System.State]
        FROM WorkItems
        WHERE 
            [System.AssignedTo] = '{assigned_to_email}'
        AND 
            [System.State] NOT IN ('Closed', 'Done', 'Removed', 'Resolved')
        ORDER BY [System.ChangedDate] DESC
        """
    }

    

    wiql_url = (
        f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1"
    )

    # Execute WIQL
    wiql_response = requests.post(wiql_url, json=wiql, headers=headers, verify=False)

    if wiql_response.status_code != 200:
        print("[ERROR] WIQL query failed:", wiql_response.text)
        return []

    work_item_refs = wiql_response.json().get("workItems", [])
    if not work_item_refs:
        print("[INFO] No unresolved tasks assigned to you.")
        return []

    # Fetch work items by ID list
    ids = ",".join(str(w["id"]) for w in work_item_refs)
    items_url = (
        f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?"
        f"ids={ids}&$expand=fields&api-version=7.1-preview.3"
    )

    items_response = requests.get(items_url, headers=headers, verify=False)

    if items_response.status_code != 200:
        print("[ERROR] Failed to fetch work item details:", items_response.text)
        return []

    items = items_response.json().get("value", [])
    tasks = []

    for item in items:
        fields = item.get("fields", {})

        save_task({
            "id": item.get("id"),
            "source": "Azure DevOps",
            "title": fields.get("System.Title"),
            "description": fields.get("System.Description"),
            "state": fields.get("System.State"),
            "assigned_to": fields.get("System.AssignedTo", {}).get("uniqueName"),
            "due_date": fields.get("Microsoft.VSTS.Scheduling.DueDate"),
            "urgency": fields.get("Microsoft.VSTS.Common.Priority"),
            "type": fields.get("System.WorkItemType"),
        })

    print(f"[INFO] Retrieved {len(tasks)} DevOps tasks.")
    return tasks