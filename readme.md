🗂 1. Project Structure

workman/
│
├── cli.py
├── config.py
│
├── azure/
│   ├── __init__.py
│   ├── client.py
│   ├── group/
│   │   ├── __init__.py
│   │   ├── create.py
│   │   ├── add_role.py
│   │   └── delete.py
│   ├── storage/
│   │   ├── __init__.py
│   │   └── add_role.py
│   └── rbac/
│       ├── __init__.py
│       └── assign.py
│
├── databricks/
│   ├── __init__.py
│   ├── client.py
│   ├── cluster/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   └── restart.py
│   ├── jobs/
│   │   ├── __init__.py
│   │   └── run.py
│   └── permissions/
│       ├── __init__.py
│       └── set.py
│
├── adf/
│   ├── __init__.py
│   ├── client.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── run.py
│   ├── trigger/
│   │   ├── __init__.py
│   │   └── start.py
│   └── linked_service/
│       ├── __init__.py
│       └── test.py
│
└── pyproject.toml


Key Features of This Codebase
	•	Nested per-resource files (Option A)
	•	Azure CLI commands: group, storage, rbac
	•	Databricks CLI commands: cluster, jobs, permissions
	•	ADF CLI commands: pipeline, trigger, linked-service
	•	Config system for defaults (~/.wm/config.json)
	•	DefaultAzureCredential auth for Azure & shared with ADF
	•	Token-based auth for Databricks
	•	Fully Typer-powered CLI with proper subcommands
	•	Scalable and extendable


Usage Examples

Set default subscription & Databricks host/token

wm config set azure.subscription_id <sub>
wm config set databricks.host https://adb-xxxx.azuredatabricks.net
wm config set databricks.token <token>

Azure

wm azure group create myrg --location westus
wm azure group add-role myrg <principal> <roleDefId>
wm azure storage add-role mystorage myrg <principal> <roleDefId>

Databricks

wm databricks cluster start <cluster-id>
wm databricks jobs run <job-id>
wm databricks permissions set /Users/me notebook principal CanEdit

ADF

wm adf pipeline run myPipe --rg data-rg --factory factory1
wm adf trigger start nightly --rg data-rg --factory factory1
wm adf linked-service test AzureBlobLS --rg data-rg --factory factory1






# High-Level Flow

+---------------------+
|  Data Sources       |
|  (Outlook, Teams,   |
|   DevOps, ServiceNow|
|   Calendar)         |
+----------+----------+
           |
           v
+---------------------+
|  Fetch & Normalize  |
|  (Pull messages,    |
|   tasks, tickets)   |
+----------+----------+
           |
           v
+---------------------+
|  Task Extraction &  |
|  Triage             |
|  - AI summarizes    |
|  - Detect actionable|
|  - Prioritize tasks |
+----------+----------+
           |
           v
+---------------------+
|  AI Action Generator|
|  - Draft replies    |
|  - Summaries        |
|  - Suggestions      |
+----------+----------+
           |
           v
+---------------------+
|  Approval Dashboard |
|  - Approve/Edit/Reject|
|  - Visual task list |
+----------+----------+
           |
           v
+---------------------+
|  Execution Engine   |
|  - Save draft       |
|  - Update ticket    |
|  - Send approved msg|
+---------------------+
           |
           v
+---------------------+
|  Logging & Memory   |
|  - DB for tasks, AI |
|  - Audit trail      |
|  - Historical context|
+---------------------+
