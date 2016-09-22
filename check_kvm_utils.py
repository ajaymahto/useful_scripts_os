# Script to get vm_ip and other details from vm_name, using simple curl, 
# when trying from a non-controller node.
#! /usr/bin/env python

import sys
import json
import socket
from subprocess import Popen, PIPE

# function to get token from keystone.
def get_token(controller, username, password):
 token_command = "curl -d '{\"auth\":{\"passwordCredentials\": \
                  {\"username\": \"%s\",\"password\": \"%s\"}, \
                  \"tenantName\": \"admin\"}}' -H \"Content-Type: \
                  application/json\" http://%s:5000/v2.0/tokens \
                  | python -m json.tool" % (username, password, controller)

 p = Popen(token_command, shell=True, stdout=PIPE, stderr=PIPE)
 output, err = p.communicate()
 my_dict = json.loads(output)
 token = my_dict['access']['token']['id']
 return token

# function to get admin_tenant_id.
def get_admin_tenant_id(controller, token):
 command_for_admin_id = "curl -s -H \"X-Auth-Token: %s\" \
                         http://%s:35357/v2.0/tenants | \
                         python -m json.tool" % (token, controller)
 p = Popen(command_for_admin_id, shell=True, stdout=PIPE, stderr=PIPE)
 output, err = p.communicate()
 tenants = json.loads(output)
 ad_tnt = [tenant for tenant in tenants['tenants'] if tenant['name'] == "admin"]
 admin_id = ad_tnt[0]['id']
 return admin_id

# function to get vm list.
def get_vm_list(controller, username, password):
 token = get_token(controller, username, password)
 admin_tenant_id = get_admin_tenant_id(controller, token)
 command_new = "curl -s -H \"X-Auth-Token: %s\" \
                http://%s:8774/v2/%s/servers/detail?all_tenants=1 | \
                python -m json.tool" % (token, controller, admin_tenant_id)
 p = Popen(command_new, shell=True, stdout=PIPE, stderr=PIPE)
 output, err = p.communicate()
 instance_details = json.loads(output)
 hostname = socket.gethostname()
 vm_list = {}
 for instance in instance_details['servers']:
   vm_hostname = instance['OS-EXT-SRV-ATTR:hypervisor_hostname']
   name = instance['name']
   network = instance['addresses'].keys()[0]
   address = instance['addresses'][network][0]['addr']
   if hostname == vm_hostname:
     vm_list[name] = address
 return vm_list

# function to get vm_ip from vm_name.
def get_vm_ip(controller, username, password, vm_name):
 vm_list = get_vm_list(controller, username, password)
 return vm_list[vm_name]

def main():
 controller = "" # Controller VIP
 username = ""
 password = ""
 vm_name = ""
 print get_vm_list(controller, username, password)
 print get_vm_ip(controller, username, password, vm_name)

if __name__ == '__main__':
   sys.exit(main())
