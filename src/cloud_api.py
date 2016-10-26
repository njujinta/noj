#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from novaclient import exceptions
import json
import time

# our own module
from credentials import get_nova_client
from credentials import get_glance_client
from credentials import get_neutron_client
import ret_code

app = Flask(__name__)

# launch an instance and return the instance id and allocated float ip address
def launch_instance():

    # do we miss any argument?
    # if do not do this
    # the server will simply throw a 400-error to the user
    # which is not so imformative
    if 'image' not in request.form or \
            'flavor' not in request.form or \
            'internet' not in request.form or \
            'name' not in request.form:
        return json.dumps(ret_code.err_arg_missed)

    nova = get_nova_client()

    # sanity check
    try:
        # print request.form['image']
        image = nova.images.find(name = request.form['image'])
    except exceptions.NotFound, msg:
        print msg
        return json.dumps(ret_code.err_inval_image)

    try:
        # print request.form['flavor']
        flavor = nova.flavors.find(name = request.form['flavor'])
    except exceptions.NotFound, msg:
        print msg
        return json.dumps(ret_code.err_inval_flavor)

    # all the instances will be attached to the network
    net_name = 'network_oj'
    try:
        net = nova.networks.find(label = net_name)
    except exceptions.NotFound, msg:
        print msg
        return json.dumps({'ret_code':ret_code.ERR_INVAL_CLOUD_CONFIG, 
        'description':msg.message})

    nics = [{'net-id': net.id}]

    internet = request.form['internet']
    if internet == 'true':
        security_groups = ['oj_teacher']
    elif internet == 'false':
        security_groups = ['oj_exam']
    else:
        return json.dumps(ret_code.err_inval_internet)

    try:
        server = nova.servers.create(request.form['name'], image = image, 
                flavor = flavor, security_groups = security_groups, 
                nics = nics)
    except exceptions.BadRequest, msg:
        # this may happed due to non-existence of the security_group
        print msg
        # msg is a BadRequest object, it is printable but not json serializable
        # so we need to use msg.message
        return json.dumps({'ret_code':ret_code.ERR_INVAL_CLOUD_CONFIG, 
            'description':msg.message})

    server_id = server.id

    # sleep for 5 seconds and see whether we can launch it
    time.sleep(5)
    server = nova.servers.get(server_id)
    # this may encounter problems when the cloud is too slow
    # that it builds a image for more than 5 seconds and then failed
    # we may need to modify this to deal with this corner case
    if server.status == 'ERROR':
        print server_id, server.status
        nova.servers.delete(server)
        return json.dumps(ret_code.err_vm_creation_failure)

    # assign floating ips
    try:
        floating_ip = nova.floating_ips.create(pool = 'EXT_01')
    except exceptions.NotFound, msg:
        # EXT_01 does not exist!
        print msg
        # do not forget to release resources
        nova.servers.delete(server)
        return json.dumps({'ret_code':ret_code.ERR_INVAL_CLOUD_CONFIG, 'description':msg.message})

    server.add_floating_ip(address = floating_ip)

    return json.dumps({'ret_code':ret_code.RET_SUCCESS, 'description':'Success', 
        'vm_id':server_id, 'vm_ip':floating_ip.ip})


dispatch_table = {
        'launch_instance':launch_instance
        }

@app.route('/cloud_api', methods=['POST'])
def dispatcher():
    # the user posted form is request.form
    if 'command' not in request.form:
        return json.dumps(ret_code.err_inval_cmd)

    command = request.form['command']
    if command not in dispatch_table:
        return json.dumps(ret_code.err_inval_cmd)
    else:
        return dispatch_table[command]()


if __name__ == '__main__':
    app.run()
