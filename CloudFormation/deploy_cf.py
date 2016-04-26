#!/usr/bin/env python 

import boto3

cf = boto3.resource('cloudformation')
for stack in cf.stacks.all():
    print(stack)

response = cf.meta.client.validate_template(
    #TemplateBody='string',
    TemplateURL='https://s3-us-west-2.amazonaws.com/ch-cf-template/lab1-vpc_ELB_combined.template'
)

print response
