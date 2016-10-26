#!/bin/bash
# missing command
http -f POST 127.0.0.1:5000/cloud_api hello=world
# invalid command
http -f POST 127.0.0.1:5000/cloud_api command=hello
# argument missed
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true
# invalid image name
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-desktop-x86 flavor=m1.small internet=true name=test
# invalid flavor
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.miao internet=true name=test
# invalid internet setting
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=miao name=test

# I haven't thought out an elegant way to test whether we can deal with invalid cloud configurations
# you need to manually modify the code in cloud_api to do this
# for example, change the network_name to a invalid one
# and see whether we catch it

# launch up to 6 instances and see whether we can launch it
# if it fails, is the failed instance removed properly?
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image=xubuntu-14.04-desktop-x86 flavor=m1.small internet=true name=test

# log into your dashboard and do some necessary cleaning
