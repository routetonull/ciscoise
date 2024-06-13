'''
getisenodes.py

Print a list of ISE nodes connected to a cluster.

Output format:
name,fqdn,nodeServiceTypes,ipAddress

Requires IP and credentials.

Option 1: use ENV vars:

export ise_ip=<ISE IP address>
export ise_username=<ISE username>
export ise_password=<ISE password>

Option 2: add IP and credentials in code (not recommended)

'''
import httpx
import os

def printNodeDetails(node_details):
    name = node_details.get('Node').get('name')
    fqdn = node_details.get('Node').get('fqdn')
    ip = node_details.get('Node').get('ipAddress')
    roles = node_details.get('Node').get('nodeServiceTypes').replace(",","-").replace(" ","_")
    print(f"{name},{fqdn},{roles},{ip}")

########## SET LOGIN CREDENTIALS AND ADMIN NODE IP
ise_ip = os.environ.get("ise_ip") if os.environ.get("ise_ip") else None
ise_username = os.environ.get("ise_username") if os.environ.get("ise_username") else None
ise_password = os.environ.get("ise_password") if os.environ.get("ise_password") else None

if not (ise_ip and ise_username and ise_password):
    raise Exception("missing input IP or credentials")
    
# define ISE API URL
ise_url = f"https://{ise_ip}:9060"

# Define the endpoint URL for listing nodes
url = f"{ise_url}/ers/config/node"

# Make the GET request to list nodes
response = httpx.get(url, auth=(ise_username, ise_password), headers={"Accept": "application/json"}, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    nodes = response.json()
    # Print or log the nodes to find the node ID
    #print(nodes)
    #for node in nodes.get('SearchResult', {}).get('resources', []):
    #    print(f"Node ID: {node.get('id')}")
    for node in nodes.get('SearchResult', {}).get('resources', []):
        #print(node)
        node_id = node.get('id')
        url = f"{ise_url}/ers/config/node/{node_id}"
        response = httpx.get(url, auth=(ise_username, ise_password), headers={"Accept": "application/json"}, verify=False)
        if response.status_code == 200:
            # Parse the JSON response
            node_details = response.json()
            #print(node_details)
            printNodeDetails(node_details)
        else:
            print(f"Failed to retrieve node {node_id} details. Status code: {response.status_code}")
            print(response.text)
else:
    print(f"Failed to retrieve nodes. Status code: {response.status_code}")
    print(response.text)