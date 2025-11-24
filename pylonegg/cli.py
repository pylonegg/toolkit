import typer
import logging
from pylonegg.databricks import databricks_app
from pylonegg.datafactory import datafactory_app
from pylonegg.azure import azure_app
from pylonegg.config import config_app


# --- Logging configuration --------------------
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


# --- Typer configuration --------------------
app = typer.Typer(help="Pylonegg - Cloud Operations Toolkit")
app.add_typer(databricks_app, name="databricks")
app.add_typer(datafactory_app, name="datafactory")
app.add_typer(azure_app, name="azure")
app.add_typer(config_app, name="config")


if __name__ == "__main__":
    app()