# snapshotylzer-3000

demo for aws snapshot stuff

## About

This project uses boto3 to manage ec2 instances

## Configuration

shotty uses the configuration file craeted by the AWS cli e.g. 
`aws configure --profile shotty`

## Running

`pipenv run python shotty/shotty.py <command> <--project=PROJECT>`

*command* is list,start, or stop
*project* is optional