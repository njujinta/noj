#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keystoneauth1 import loading
from keystoneauth1 import session
import novaclient.client as nova_client
import glanceclient.client as glance_client
import neutronclient.v2_0.client as neutron_client

import os

# I think it's not a good idea to let the user change the code to provide their credentials
# instead, I think the user should just source their own openstack-rc file
# and then everything works
def get_session():
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(
            auth_url = os.environ['OS_AUTH_URL'],
            username = os.environ['OS_USERNAME'],
            password = os.environ['OS_PASSWORD'],
            project_id = os.environ['OS_TENANT_ID'])
    return session.Session(auth = auth)

def get_nova_client():
    VERSION = '2'
    sess = get_session()
    return nova_client.Client(VERSION, session = sess)

def get_glance_client():
    VERSION = '2'
    sess = get_session()
    return glance_client.Client(VERSION, session = sess)

def get_neutron_client():
    sess = get_session()
    return neutron_client.Client(session = sess)
