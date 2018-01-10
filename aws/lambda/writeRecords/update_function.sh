#!/bin/bash

aws lambda update-function-code \
  --function-name writeRecords \
  --zip-file fileb://writeRecords.zip
