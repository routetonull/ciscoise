'''
getiallcerts.py

Print a list of ISE certificates on all nodes

Format:

hostname!friendlyName!issuedTo!issuedBy!validFrom!expirationDate!usedBy!serialNumber

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

def getNodeDetails(nodes):
    """
    return a dictionary with node details
    """
    details={}
    details['name'] = node_details.get('Node').get('name')
    details['fqdn'] = node_details.get('Node').get('fqdn')
    details['ip'] = node_details.get('Node').get('ipAddress')
    details['roles'] = node_details.get('Node').get('nodeServiceTypes').replace(",","-").replace(" ","_")
    return details
    
def getCerts(ise_ip,username,password,node):
    """
    provide node hostname
    return node certificates details
    """
    certificates=[]
    cert_endpoint = f"https://{ise_ip}/api/v1/certs/system-certificate/{{hostname}}"
    response = httpx.get(cert_endpoint.format(hostname=node), auth=(username, password), verify=False)
    if response.status_code == 200:
        certs = response.json()
        #print("hostname,friendlyName,issuedTo,issuedBy,validFrom,expirationDate,usedBy")
        for cert in certs.get('response'):
        #print(cert)
            friendlyName = cert.get('friendlyName')
            issuedTo = cert.get('issuedTo')
            issuedBy = cert.get('issuedBy')
            validFrom = cert.get('validFrom')
            expirationDate = cert.get('expirationDate')
            usedBy = cert.get('usedBy')
            serialNumber = cert.get('serialNumberDecimalFormat')
            certificates.append(f"{node}!{friendlyName}!{issuedTo}!{issuedBy}!{validFrom}!{expirationDate}!{usedBy}!{serialNumber}")
        return certificates    
    else:
        return 1

########## SET LOGIN CREDENTIALS AND ADMIN NODE IP
ise_ip = os.environ.get("ise_ip") if os.environ.get("ise_ip") else None
ise_username = os.environ.get("ise_username") if os.environ.get("ise_username") else None
ise_password = os.environ.get("ise_password") if os.environ.get("ise_password") else None

if not (ise_ip and ise_username and ise_password):
    raise Exception("missing input IP or credentials")
    
# define ISE API URL
ise_server = f"https://{ise_ip}:9060"

print("hostname!friendlyName!issuedTo!issuedBy!validFrom!expirationDate!usedBy!serialNumber")

# Define the endpoint URL for listing nodes
url = f"{ise_server}/ers/config/node"

# Make the GET request to list nodes
response = httpx.get(url, auth=(ise_username, ise_password), headers={"Accept": "application/json"}, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    nodes = response.json()
    for node in nodes.get('SearchResult', {}).get('resources', []):
        nodeName = node.get('name')
        certificates = getCerts(ise_ip,ise_username,ise_password,nodeName)
        for certificate in certificates:
            print(certificate)