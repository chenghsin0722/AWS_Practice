#!/usr/bin/env python 

import time
import sys
import boto3
import json

S3Bucket = "ch-cf-template"

def get_stack_info(cfClient, stackID):
    response = cfClient.describe_stacks(StackName = stackID)
    if len(response["Stacks"]) == 1:
        return response["Stacks"][0]
    else:
        raise "STACK IS NOT FOUND"

def wait_for_stack_created(cfClient,stackID):
    stackInfo = get_stack_info(cfClient, stackID)
    while stackInfo["StackStatus"] == "CREATE_IN_PROGRESS":
        print("stack ID: " + stackID + " status: " + stackInfo["StackStatus"])
        time.sleep(10)
        stackInfo = get_stack_info(cfClient, stackID)
        if(stackInfo["StackStatus"] == "CREATE_COMPLETE"):
            print("stack " + stackInfo["StackName"] + " is created successfully")
        else:
            print("FAIL TO CREATE STACK " + stackID + " status: " + stackInfo["StackStatus"]);
    sys.exit(1)

def create_stack(cfClient,stackname, templateURL):
    response = cfClient.create_stack(
	StackName = stackname,
	TemplateURL= templateURL,
    )
    print("StackID: " + response["StackId"])
    return response["StackId"]

def uploadcf(cftemplate):
    s3client = boto3.client('s3')

    #no status check?
    s3client.upload_file(cftemplate, S3Bucket, cftemplate)
    down_url = s3client.generate_presigned_url('get_object', \
    	Params={'Bucket': S3Bucket, 'Key': cftemplate},ExpiresIn= 3600)
    return down_url

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'Usage: python deploy_cf.py [cf template] [cf name]'
        sys.exit(-1)

    tmpurl = uploadcf(sys.argv[1])
    
    cfClient = boto3.client('cloudformation')
    stackID = create_stack(cfClient,sys.argv[2], tmpurl)
    wait_for_stack_created(cfClient, stackID)

