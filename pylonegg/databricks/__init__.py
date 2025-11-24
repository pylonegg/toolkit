import typer 
from pylonegg.databricks.cluster.start import *

# -----------------------------
# Databricks CLI group
# -----------------------------
databricks_app = typer.Typer(help="Databricks operations")

cluster_app = typer.Typer(help="Cluster operations")
databricks_app.add_typer(cluster_app, name="cluster")

jobs_app = typer.Typer(help="Job operations")
databricks_app.add_typer(jobs_app, name="jobs")

perm_app = typer.Typer(help="Permissions operations")
databricks_app.add_typer(perm_app, name="permissions")

@cluster_app.command("test")
def testing():
    print("Hello world")


# @cluster_app.command("start")
# def cli_start_cluster(cluster_id: str, host: str = None, token: str = None):
#     host = host or get("databricks.host")
#     token = token or get("databricks.token")
#     start_cluster(host, token, cluster_id)
#     typer.echo(f"Cluster {cluster_id} started.")

# @cluster_app.command("restart")
# def cli_restart_cluster(cluster_id: str, host: str = None, token: str = None):
#     host = host or get("databricks.host")
#     token = token or get("databricks.token")
#     restart_cluster(host, token, cluster_id)
#     typer.echo(f"✔ Cluster {cluster_id} restarted.")

# @jobs_app.command("run")
# def cli_run_job(job_id: str, host: str = None, token: str = None):
#     host = host or get("databricks.host")
#     token = token or get("databricks.token")
#     run_job(host, token, job_id)
#     typer.echo(f"✔ Job {job_id} triggered.")

# @perm_app.command("set")
# def cli_set_permission(object_path: str, principal: str, permission: str, host: str = None, token: str = None):
#     host = host or get("databricks.host")
#     token = token or get("databricks.token")
#     set_permission(host, token, object_path, principal, permission)
#     typer.echo(f"✔ Permission set on {object_path}.")
