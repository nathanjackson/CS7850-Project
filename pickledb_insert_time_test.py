#!/usr/bin/env python3

import random
import string
import timeit
import uuid

from argparse import ArgumentParser

import pickledb

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the pickledb insert test")
    args = ap.parse_args()

    db = pickledb.load("insert_time.db", False)

    output_file = open("insert_time_pickledb.csv", "w")

    inserts = 1000000
    for i in range(inserts):
        key = uuid.uuid4()
        def do_put():
            db.set(str(key), randomString())
        duration = timeit.timeit(do_put, number=1)
        output_file.write("%i,%f\n" % (i+1, duration))
        if 0 == i % 1000:
            print("inserts %d / %d" % (i, inserts))

    db.dump()

    output_file.close()
