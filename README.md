# CS7850 Project

Key-Value store based on Path ORAM. The Key-Value store code is stored in the
`privatekv` module. Some basic unit tests are also provided. The key-value store
code itself was implemented by me as were the unit tests. All experiments were
written by me as well.

I made use of PickleDB (https://pythonhosted.org/pickleDB/) for comparion
purposes as well as the Amazon Web Service (AWS) `boto3` library.

The Path ORAM implementation is provided by PyORAM: https://github.com/ghackebeil/PyORAM.

## General Notes

PyORAM provides the ability to use S3, SFTP, a local file, or RAM as the backing
store. In practice, it seems that SFTP backend is broken as I couldn't get it
to work. All experiments use a local file, RAM, or Amazon S3. The KV Store
itself may be implemented on top of any of these back ends as the Path ORAM
interface is the same.

All code is written in Python 3.

All experiments were done on a computer with the following specifications:

- Intel Core i7-4770
- 32GB of DDR3-1600  RAM
- Fedora 30

If you were going to actually use this code, you currently would have to
disable Python's random salting of the built in hash function. See:
https://stackoverflow.com/questions/27522626/hash-function-in-python-3-3-returns-different-results-between-sessions

## Installing Dependencies

I recommend setting up a virtual environment to install dependencies. This
allows you to remove easily the dependenices later. Follow these instructions
to setup the virtual environemnt.

All experiments and other instructions assume you've already run these steps.

1. Install `virtualenv` (Fedora 30 specific).

    ```
    sudo dnf install python3-virtualenv
    ```

2. Create virtual environment.

    ```
    virtualenv venv
    ```

3. Activate the virtual environment.

    ```
    . ./venv/bin/activate
    ```

4. Install dependencies.

    ```
    pip3 install -r requirements.txt
    ```

## Run Unit Tests

Assuming you've already activated the virtual environment with depdencies, you
can just run the unit tests like so:

```
./tests/test.py
```

## Experiment 1

This experiment is modeled after the Path ORAM Bucket Load test found in the
Path ORAM paper. More details can be found in the final report. These
instructions only describe how to re-run the tests.

Be advised, each step takes roughly one hour to complete.

1. Run the bucket load test with a bucket size (Z) equal to 3.

    ```
    ./bucket_load_test.py -z 3
    ```

    Record the output (if required).

2. Run the bucket load test with a bucket size (Z) equal to 4.

    ```
    ./bucket_load_test.py -z 4
    ```

    Record the output (if required).

3. Run the bucket load test with a bucket size (Z) equal to 5.

    ```
    ./bucket_load_test.py -z 5
    ```

    Record the output (if required).

## Experiment 2

This experiment is designed to determine how much client storage is needed in
the worst case.

Be advised, each step takes roughly one hour to complete.

1. Run the max stash size test with 16384 blocks.

    ```
    ./max_stash_size_test.py -n 16384
    ```

    Record the output (if required).

2. Run the max stash size test with 32768 blocks.

    ```
    ./max_stash_size_test.py -n 32768
    ```

    Record the output (if required).

3. Run the max stash size test with 65536 blocks.

    ```
    ./max_stash_size_test.py -n 65536
    ```

    Record the output (if required).

## Experiment 3

This experiment is designed to test the insert performance locally across a few
number of buckets.

Again, each step takes roughly one hour to complete.

The output of each step is a CSV file containing the insert times.

1. Run the local insert performance test with 16384 buckets.

    ```
    ./insert_time_test.py -n 16384
    ```

2. Run the local insert performance test with 32768 buckets.

    ```
    ./insert_time_test.py -n 32768
    ```

3. Run the local insert performance test with 65536 buckets.

    ```
    ./insert_time_test.py -n 65536
    ```

4.  Run the PickleDB insert performance test.

    ```
    ./pickledb_insert_time_test.py
    ```

## Experiment 4

This experiment is designed to test the insert performance where the Path ORAM
is stored in Amazon S3.

You must set the following environment variables first:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

These values must come from the AWS console. The user you create in the console
needs to have full permissions to an S3 bucket and DynamoDB.

The output of each step is a CSV file containing the insert times.

1. Run the S3 insert time test with no local caching.

    ```
    ./s3_insert_time_test.py -c 0 -b <Bucket Name>
    ```

2. Run the S3 insert time test 3 cached levels levels.

    ```
    ./s3_insert_time_test.py -c 3 -b <Bucket Name>
    ```

3. Run the S3 insert time test 8 cached levels levels.

    ```
    ./s3_insert_time_test.py -c 8 -b <Bucket Name>
    ```

4. Run the DynamoDB insert test.

    ```
    ./dynamodb_insert_time_test.py
    ```

## Experiment 5

This experiment is designed to compare the number of GET and PUT requests on a
per-block level to S3. This is used to check for access patterns.

You must set the following environment variables first:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

These values must come from the AWS console. The user you create in the console
needs to have full permissions to an S3 bucket.

Additionally, you must enable S3 access logging. See here:
https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html

1. Setup the Path ORAM store first with this command:

    ```
    PYTHONHASHSEED=0 ./s3_access_log_test.py --create -b <Bucket Name>
    ```

2. Enable S3 server side logging on the bucket. See here:

    https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html

3. Execute the actual test.

    ```
    PYTHONHASHSEED=0 ./s3_access_log_test.py -b <Bucket Name>
    ```

4. Wait about 1 hour for the logs to show up in the S3 Bucket and then download the S3 logs.

    ```
    for log in $(aws s3 ls s3://<Bucket Name> | awk '{print $4}'); do aws s3 cp s3://<Bucket Name>/$log logs/; echo $log; done
    ```

    Log data was used to construct experiment 5 results.
