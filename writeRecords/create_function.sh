#!/bin/bash

subnet_ids=`aws ec2 describe-subnets | jq -r '.Subnets|map(.SubnetId)|join(",")'`
sg_id="sg-ac912cd0"

aws lambda create-function \
    --region us-west-2 \
    --profile default \
    --function-name writeRecords \
    --zip-file fileb://writeRecords.zip \
    --role arn:aws:iam::490069154287:role/lambda-writeRecords-role \
    --handler writeRecords.lambda_handler \
    --runtime python3.6 \
    --timeout 60 \
    --memory-size 1024 \
    --vpc-config SubnetIds="${subnet_ids}",SecurityGroupIds="${sg_id}"

