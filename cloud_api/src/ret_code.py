#!/usr/bin/env python
# -*- coding: utf-8 -*-

# does python have enumeration?
RET_SUCCESS = 0
ERR_INVAL_CMD = 1
ERR_ARG_MISSED = 2
ERR_INVAL_IMAGE = 3
ERR_INVAL_FLAVOR = 4
ERR_INVAL_INTERNET = 5
ERR_INVAL_VM_ID = 6
ERR_VM_CREATION_FAILURE = 7
# error due to invalid cloud platform configurations, 
# such as no security_groups, no external ip address pool
ERR_INVAL_CLOUD_CONFIG = 8

err_inval_cmd = {'ret_code':ERR_INVAL_CMD, 'description':'Invalid command'}
err_arg_missed = {'ret_code':ERR_ARG_MISSED, 'description':'Argument missing'}
err_inval_image = {'ret_code':ERR_INVAL_IMAGE, 'description':'Invalid image name'}
err_inval_flavor = {'ret_code':ERR_INVAL_FLAVOR, 'description':'Invalid flavor name'}
err_inval_internet = {'ret_code':ERR_INVAL_INTERNET, 'description':'Invalid internet access setting'}
err_vm_creation_failure = {'ret_code':ERR_VM_CREATION_FAILURE, 'description':'Virtual machine creation failed'}
