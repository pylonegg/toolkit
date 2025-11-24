import requests

def start_cluster(host: str, token: str, cluster_id: str):
    url = f"{host}/api/2.0/clusters/start"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, json={"cluster_id": cluster_id})
    resp.raise_for_status()
    return resp.json()


def test_function():
    print("Test sucessful")

# Other Databricks modules (restart.py, jobs/run.py, permissions/set.py) are similar.