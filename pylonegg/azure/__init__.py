import typer
from pylonegg.azure.resourcegroup.create import create_group
from pylonegg.azure.storage.sync import copy_storage

# -----------------------------
# Azure CLI group
# -----------------------------
azure_app = typer.Typer(help="Azure operations")

group_app = typer.Typer(help="Resource Group operations")
azure_app.add_typer(group_app, name="group")

storage_app = typer.Typer(help="Storage operations")
azure_app.add_typer(storage_app, name="storage")

rbac_app = typer.Typer(help="RBAC operations")
azure_app.add_typer(rbac_app, name="rbac")

@group_app.command("test")
def testing():
    print("Hello world")




# Group commands
# @group_app.command("create")
# def cli_create_group(name: str, location: str = typer.Option("westeurope"), subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     create_group(name, location, subscription)
#     typer.echo(f"✔ Resource Group '{name}' created.")

# @group_app.command("add-role")
# def cli_group_add_role(name: str, principal_id: str, role_definition_id: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     add_role_group(name, principal_id, role_definition_id, subscription)
#     typer.echo(f"✔ Role assigned to RG '{name}'.")

# # Storage commands
# @storage_app.command("add-role")
# def cli_storage_add_role(account: str, rg: str, principal_id: str, role_definition_id: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     add_role_storage(account, rg, principal_id, role_definition_id, subscription)
#     typer.echo(f"✔ Role assigned to storage account '{account}'.")

# Storage commands
@storage_app.command("sync")
def cli_storage_copy():
    copy_storage()


# # RBAC generic
# @rbac_app.command("assign")
# def cli_rbac_assign(principal_id: str, role_definition_id: str, scope: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     assign_rbac(principal_id, role_definition_id, scope, subscription)
#     typer.echo(f"✔ Role assigned on scope '{scope}'.")