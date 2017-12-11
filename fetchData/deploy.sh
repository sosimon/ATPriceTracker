#!/bin/bash

aws lambda create-function \
    --region us-west-2 \
    --function-name fetchData \
    --zip-file file://home/ec2-user/fetchData.zip \
    --role arn:aws:iam::490069154287:role/lambda-execution-role \
    --handler fetchData.lambda_handler \
    --runtime python3.6 \
    --profile adminuser \
    --timeout 10 \
    --memory-size 1024

