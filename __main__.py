"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

import pulumi
import pulumi_aws as aws

# Define the *existing* VPC so foundation can adopt it (import step below).
# Fill these to match the real VPC so Pulumi doesn't try to replace it.
vpc = aws.ec2.Vpc(
    "app-vpc",
    cidr_block="10.0.0.0/16",          # <-- replace with your actual CIDR
    enable_dns_support=True,           # <-- match real attributes
    enable_dns_hostnames=True,         # <-- match real attributes
    tags={"Name": "penobscot-app-vpc"},
)

pulumi.export("vpcId", vpc.id)
pulumi.export("vpcCidr", vpc.cidr_block)
