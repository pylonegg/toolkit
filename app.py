import typer
import logging
from pylonegg.config import config_app, load_config
from pylonegg.storage import copy_storage
from pylonegg.agent import main

# --- Configuration --------------------
logging.basicConfig(
    filename="./log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Suppress Azure SDK verbose logging
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)

# Load configuration
try:
    config = load_config()
    config['config_version']
except Exception as e:
    print("Error loading configuration")

# Typer App
app = typer.Typer(help="Pylonegg - Cloud Operations Toolkit")
app.add_typer(config_app, name="config")





# ===== Agent ====================================
agent_app = typer.Typer(help="AI Agent operations")
app.add_typer(agent_app, name="agent")

@agent_app.command("run")
def agent_run():
    main()


# ===== Azure Resources ==========================

group_app = typer.Typer(help="Resource Group operations")
app.add_typer(group_app, name="az-group")

storage_app = typer.Typer(help="Storage operations")
app.add_typer(storage_app, name="az-storage")

rbac_app = typer.Typer(help="RBAC operations")
app.add_typer(rbac_app, name="az-rbac")

@group_app.command("test")
def testing():
    print("Hello world")


@storage_app.command("sync")
def cli_storage_copy():
    copy_storage()



# ===== Databricks  ================================

from pylonegg import databricks

# --- Databricks -----------------------------------
databricks_app = typer.Typer(help="Databricks Operations")
app.add_typer(databricks_app, name="databricks")

# --- Databricks Create ------------------------------
databricks_create_app = typer.Typer(help="Databricks Create Operations")
databricks_app.add_typer(databricks_create_app, name="create")

@databricks_create_app.command("user")
def databricks_create_user(email: str = typer.Option(..., "--email", "-e", help="User email"), display_name: str = typer.Option(None, "--name", "-n", help="Display name"),):
    databricks.create_user(
        databricks_host = config["dbx_workspace_url"],
        token           = config["dbx_token"],
        email           = email
        )

@databricks_create_app.command("external-location")
def databricks_create_external_location(container: str = typer.Option(..., "--container", "-c", help="Container name"),
                                        comment: str = typer.Option(None, "--comment", "-m", help="Comment"),
                                        force: bool = typer.Option(False, "--force", "-f", help="Force creation if exists")):
    databricks.create_external_location(
        databricks_host = config["dbx_workspace_url"],
        token           = config["dbx_token"],
        storage_account = config["dbx_storage_account"],
        container       = container,
        comment         = comment,
        force           = force
        )


# --- Databricks Add ------------------------------
databricks_add_app = typer.Typer(help="Databricks Group Operations")
databricks_app.add_typer(databricks_add_app, name="add")

@databricks_add_app.command("group-user")
def databricks_add_group_user(email: str = typer.Option(..., "--email", "-e", help="User email"), group: str = typer.Option(None, "--group", "-g", help="Group name"),):
    databricks.group_add_user(
        databricks_host = config["dbx_workspace_url"],
        token           = config["dbx_token"],
        user_email      = email,
        group_name      = group
        )
    


# --- Databricks Show ------------------------------
databricks_show_app = typer.Typer(help="Databricks Show Operations")
databricks_app.add_typer(databricks_show_app, name="show")

@databricks_show_app.command("user")
def databricks_show_user(email: str = typer.Option(..., "--email", "-e", help="User email")):
    databricks.show_user(
        databricks_host = config["dbx_workspace_url"],
        token           = config["dbx_token"],
        email      = email
        )



if __name__ == "__main__":
    app()