🗂 1. Project Structure

orionflow/
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
	•	Config system for defaults (~/.orionflow/config.json)
	•	DefaultAzureCredential auth for Azure & shared with ADF
	•	Token-based auth for Databricks
	•	Fully Typer-powered CLI with proper subcommands
	•	Scalable and extendable


Usage Examples

Set default subscription & Databricks host/token

orionflow config set azure.subscription_id <sub>
orionflow config set databricks.host https://adb-xxxx.azuredatabricks.net
orionflow config set databricks.token <token>

Azure

orionflow azure group create myrg --location westus
orionflow azure group add-role myrg <principal> <roleDefId>
orionflow azure storage add-role mystorage myrg <principal> <roleDefId>

Databricks

orionflow databricks cluster start <cluster-id>
orionflow databricks jobs run <job-id>
orionflow databricks permissions set /Users/me notebook principal CanEdit

ADF

orionflow adf pipeline run myPipe --rg data-rg --factory factory1
orionflow adf trigger start nightly --rg data-rg --factory factory1
orionflow adf linked-service test AzureBlobLS --rg data-rg --factory factory1