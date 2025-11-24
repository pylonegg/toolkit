from pylonegg.azure.client import get_clients

def create_group(name: str, location: str, subscription: str):
    clients = get_clients(subscription)
    clients["rg"].resource_groups.create_or_update(name, {"location": location})
    return name