#!/usr/bin/env python3

import random
import string
import timeit
import uuid

import boto3

from argparse import ArgumentParser

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the DynamoDB insertion performance test")
    ap.add_argument("-i", default=2000, type=int, help="number of inserts")
    args = ap.parse_args()

    print("Creating DynamoDB Test Table")
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.create_table(
        TableName="test_table",
        KeySchema=[
            {
                "AttributeName": "uuid",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "value",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "uuid",
                "AttributeType": "S"
            },
            {
                "AttributeName": "value",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    table.meta.client.get_waiter("table_exists").wait(TableName="test_table")

    output_file = open("dynamodb_insert_time.csv", "w")

    inserts = args.i
    for i in range(inserts):
        key = uuid.uuid4()
        def do_put():
            table.put_item(Item={
                "uuid": str(key),
                "value": randomString()
            })
        duration = timeit.timeit(do_put, number=1)
        output_file.write("%i,%f\n" % (i+1, duration))
        print("inserts %d / %d" % (i, inserts))
    output_file.close()
