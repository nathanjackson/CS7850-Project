# CS7850 Project

Key-Value store based on Path ORAM. The Key-Value store code is stored in the
`privatekv` module. Some basic unit tests are also provided.

The Path ORAM implementation is provided by PyORAM: https://github.com/ghackebeil/PyORAM.

## General Notes

PyORAM provides the ability to use S3, SFTP, a local file, or RAM as the backing
store. In practice, it seems that SFTP backend is broken as I couldn't get it
to work. All experiments use a local file, RAM, or Amazon S3. The KV Store
itself may be implemented on top of any of these back ends as the Path ORAM
interface is the same.

All code is written in Python 3.

All experiments were done on a computer with the following specifications:

Intel Core i7-4770
32GB of DDR3-1600  RAM
Fedora 30

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

2. Run the max stash size test with 16384 blocks.

    ```
    ./max_stash_size_test.py -n 16384
    ```

    Record the output (if required).

3. Run the max stash size test with 65536 blocks.

    ```
    ./max_stash_size_test.py -n 65536
    ```

    Record the output (if required).
