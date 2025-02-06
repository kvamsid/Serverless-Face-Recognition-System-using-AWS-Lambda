import boto3
import os
import urllib.parse
import ffmpeg
import subprocess
import math
from video_splitting_cmdline import video_splitting_cmdline

s3Client = boto3.client('s3')
outputBucket = '1229700097-stage-1'

def handler(event, context):
    print(event)
    bucketName = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print('key', key)
    download_path = '/tmp/{}'.format(os.path.basename(key))
    print('download_path', download_path)
    s3Client.download_file(bucketName, key, download_path)
    result = video_splitting_cmdline(download_path)

    for images in os.listdir(result):
        s3Client.upload_file(os.path.join(result, images), outputBucket, '{}/{}'.format(os.path.splitext(key)[0], images))
    print('OutputDir', result)