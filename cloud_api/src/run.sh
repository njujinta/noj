#!/bin/bash
# arg1: your openstack-rc file
# For the openstack_rc shell script, 
# we should use source instead of directly executing it, 
# since we need it to set environment variables.
source $1
python cloud_api.py
