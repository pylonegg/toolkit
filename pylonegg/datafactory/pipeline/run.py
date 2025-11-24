from azx.client import get_clients

def run_pipeline(subscription: str, rg: str, factory: str, pipeline_name: str):
    clients = get_clients(subscription)
    adf_client = clients["rg"]  # Use ResourceManagementClient to get factory or REST
    # Simplified example: in real code use DataFactoryManagementClient
    # trigger the pipeline via adf_client.pipelines.create_run(...)
    return pipeline_name