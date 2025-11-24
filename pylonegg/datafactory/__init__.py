import typer


# -----------------------------
# ADF CLI group
# -----------------------------
datafactory_app = typer.Typer(help="Azure Data Factory operations")

pipeline_app = typer.Typer(help="Pipeline operations")
datafactory_app.add_typer(pipeline_app, name="pipeline")

trigger_app = typer.Typer(help="Trigger operations")
datafactory_app.add_typer(trigger_app, name="trigger")

ls_app = typer.Typer(help="Linked Service operations")
datafactory_app.add_typer(ls_app, name="linked-service")

@trigger_app.command("test")
def testing():
    print("Hello world")


# @pipeline_app.command("run")
# def cli_pipeline_run(name: str, rg: str, factory: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     run_pipeline(subscription, rg, factory, name)
#     typer.echo(f"✔ Pipeline '{name}' triggered.")

# @trigger_app.command("start")
# def cli_trigger_start(name: str, rg: str, factory: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     start_trigger(subscription, rg, factory, name)
#     typer.echo(f"✔ Trigger '{name}' started.")

# @ls_app.command("test")
# def cli_test_ls(name: str, rg: str, factory: str, subscription: str = None):
#     subscription = subscription or get("azure.subscription_id")
#     test_linked_service(subscription, rg, factory, name)
#     typer.echo(f"✔ Linked Service '{name}' tested.")