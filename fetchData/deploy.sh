#!/bin/bash

aws lambda create-function \
    --region us-west-2 \
    --profile default \
    --function-name fetchData \
    --zip-file fileb://fetchData.zip \
    --role arn:aws:iam::490069154287:role/lambda-execution-role \
    --handler fetchData.lambda_handler \
    --runtime python3.6 \
    --timeout 10 \
    --memory-size 1024

