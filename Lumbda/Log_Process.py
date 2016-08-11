from __future__ import print_function

import re
import json
import uuid
import boto3

print('Loading function')

s3_client = boto3.client('s3')

def log_process(raw_path,process_path):
    inputf = open(raw_path, "r")
    ouputf = open(process_path,"wb")
    for line in inputf.readlines():
        if re.search('NOERROR',line):
            m = re.search('[a-z0-9]{32}\.hashserver.cs.trendmicro.com',line)
            ouputf.write(m.group(0))
            ouputf.write("\n")

    inputf.close()
    ouputf.close()

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key'] 
    try:
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)
        s3_client.download_file(bucket, key, download_path)
        log_process(download_path, upload_path)
        s3_client.upload_file(upload_path, 'ch-hashclean', key)
        #response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        #return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
