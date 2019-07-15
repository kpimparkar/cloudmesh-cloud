#
# python cloudmesh/compute/openstack/test_openstacksdk.py
#

from cloudmesh.management.configuration.config import Config
from pprint import pprint
import openstack
from cloudmesh.common.util import banner
from cloudmesh.common.Shell import Shell
import os

"""
see : https://docs.openstack.org/openstacksdk/latest/user/guides/compute.html
"""

"""
cloudmesh4.yaml file
        OS_AUTH_URL: https://openstack.tacc.chameleoncloud.org:5000/v2.0/tokens
        OS_USERNAME: TBD
        OS_PASSWORD: TBD
        OS_TENANT_NAME: CH-819337
        OS_TENANT_ID: CH-819337
        OS_PROJECT_NAME: CH-819337
        OS_PROJECT_DOMAIN_ID: default
        OS_USER_DOMAIN_ID: default
        OS_VERSION: liberty
        OS_REGION_NAME: RegionOne
        OS_KEY_PATH: ~/.ssh/id_rsa.pub
"""

def credentials():
    d = {}

    config = Config()["cloudmesh.cloud.chameleon.credentials"]
    d['version'] = '2'
    d['username'] = config['OS_USERNAME']
    d['password'] = config['OS_PASSWORD']
    # while libcloud uses token, here we do not use it in auth_url
    d['auth_url'] = config['OS_AUTH_URL'].replace("/tokens","")
    d['project_id'] = config['OS_TENANT_NAME']
    d['region_name'] = config['OS_REGION_NAME']
    # d['project_domain_name'] = config['OS_PROJECT_NAME']
    d['tenant_id'] = config['OS_TENANT_ID']
    return d

config = credentials()

pprint(config)

cloud = openstack.connect(**config)

pprint(dir(cloud))


if False:

    command = "openstack security group list --os-auth-url={auth_url} " \
        "--os-project-name={project_id} --os-username={username} "\
        "--os-password={password} -f=json".format(**config)
    # print (command)
    os.system(command)

    """
    [
      {
        "ID": "00555968-5dad-4544-88c9-91cff2a390e6",
        "Name": "default",
        "Description": "Default security group",
        "Project": "CH-819337",
        "Tags": []
      },
      {
        "ID": "6ae7c84f-1449-4770-9ee1-2428d0ea2513",
        "Name": "rrufael-703-couchdb",
        "Description": "Couchdb security group",
        "Project": "CH-819337",
        "Tags": []
      },
      {
        "ID": "af1480e5-2e39-4958-9ba2-81f5dd7e008f",
        "Name": "default_test",
        "Description": "Security Group",
        "Project": "CH-819337",
        "Tags": []
      },
      {
        "ID": "f881d18d-162a-4ccb-a313-b8854afaed65",
        "Name": "rlambadi-514-api",
        "Description": "Security Group",
        "Project": "CH-819337",
        "Tags": []
      }
    ]

    """

    command = "openstack security group rule list --os-auth-url={auth_url} " \
        "--os-project-name={project_id} --os-username={username} "\
        "--os-password={password} default -f=json".format(**config)
    # print (command)
    os.system(command)

    """
    [
      {
        "ID": "22849a14-7a43-486c-a14c-4096d5b69f78",
        "IP Protocol": "tcp",
        "IP Range": "0.0.0.0/0",
        "Port Range": "22:22",
        "Remote Security Group": null
      },
      {
        "ID": "553d8b40-03c6-4fba-865c-652e9a0dbf68",
        "IP Protocol": "icmp",
        "IP Range": "0.0.0.0/0",
        "Port Range": "",
        "Remote Security Group": null
      },
      {
        "ID": "5bb1d82f-9a4f-4917-9f08-efe18a5cdbb1",
        "IP Protocol": null,
        "IP Range": null,
        "Port Range": "",
        "Remote Security Group": null
      },
      {
        "ID": "9ca4177c-21f4-4450-9826-d0241840a7b4",
        "IP Protocol": "tcp",
        "IP Range": "0.0.0.0/0",
        "Port Range": "5000:5000",
        "Remote Security Group": null
      },
      {
        "ID": "b5273c23-c140-4e99-a634-46323c0945ae",
        "IP Protocol": "tcp",
        "IP Range": "0.0.0.0/0",
        "Port Range": "80:80",
        "Remote Security Group": null
      },
      {
        "ID": "c22a7681-93b0-4082-96ac-ba779a672943",
        "IP Protocol": null,
        "IP Range": null,
        "Port Range": "",
        "Remote Security Group": null
      },
      {
        "ID": "f1c86b45-5606-4844-a0b9-cad2c91bb3b5",
        "IP Protocol": "tcp",
        "IP Range": "0.0.0.0/0",
        "Port Range": "443:443",
        "Remote Security Group": null
      }
    ]
    """


if False:
    banner("Flavors")
    flavors = cloud.compute.flavors()
    for entry in flavors:
        pprint(entry)

if False:
    banner("Images")

    images = cloud.compute.images()
    for entry in images:
        pprint(entry)

if False:
    banner("Servers")

    servers = cloud.compute.servers()
    for entry in servers:
        pprint(entry)




if False: # does not work
    banner("Secrets")

    keys = cloud.key_manager.secrets()
    for entry in keys:
        print(entry)

if False:

    command = "openstack keypair list --os-auth-url={auth_url} " \
        "--os-project-name={project_id} --os-username={username} "\
        "--os-password={password} -f=json".format(**config)
    # print (command)
    r = Shell.execute(command, shell=True)
    d = eval(r)
    print (type(d))
    print (d)


"""
def list_secrets_query(conn):
    print("List Secrets:")

    for secret in conn.key_manager.secrets(
            secret_type="symmetric",
            expiration="gte:2020-01-01T00:00:00"):
        print(secret)
"""
