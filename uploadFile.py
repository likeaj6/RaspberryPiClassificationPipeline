import boto3

s3 = boto3.client('s3')
bucket_name = 'trashdataset'

def upload(filename):
    s3.upload_file(filename, bucket_name, filename)
