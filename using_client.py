#! /usr/bin/env python

import os
import sys
from keystoneclient.auth.identity.v3 import Password 
from keystoneclient import session
from keystoneclient import client
from keystoneclient.v3 import client

def main():
  auth = Password(auth_url=os.environ['OS_AUTH_URL'], \
                  password=os.environ['OS_PASSWORD'], \
                  username=os.environ['OS_USERNAME'], \
                  user_domain_id=os.environ['OS_USER_DOMAIN_ID'], \
                  project_name=os.environ['OS_PROJECT_NAME'], \
                  project_domain_id=os.environ['OS_PROJECT_DOMAIN_ID'])
  
  sess = session.Session(auth=auth)
  kc = client.Client(session=sess)
  project_list = kc.projects.list()
  

  for project in project_list:
     print project, "\n"
  print len(kc.projects.list())

if __name__ == "__main__":
   sys.exit(main())
