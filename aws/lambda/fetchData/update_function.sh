#!/bin/bash

aws lambda update-function-code \
  --function-name fetchData \
  --zip-file fileb://fetchData.zip
