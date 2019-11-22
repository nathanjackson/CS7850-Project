#!/usr/bin/env python3

import random
import string
import timeit
import uuid

from argparse import ArgumentParser

import pyoram

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store
import privatekv.utils

BLOCK_COUNT = 512
BLOCK_SIZE = 4096

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the PrivateKV S3 insertion performance test")
    ap.add_argument("-c", default=0, type=int, help="cached levels")
    ap.add_argument("-b", default="test", help="the S3 bucket to use")
    ap.add_argument("-i", default=2000, type=int, help="number of inserts")
    args = ap.parse_args()

    print("Setting up ORAM")
    pyoram.config.SHOW_PROGRESS_BAR = True
    oram = PathORAM.setup("test", BLOCK_SIZE, BLOCK_COUNT, cached_levels=args.c, storage_type="s3",
                          bucket_name=args.b, ignore_existing=True)
    pyoram.config.SHOW_PROGRESS_BAR = False
    kv = privatekv.store.KVORAM(oram)
    output_file = open("s3_insert_time.csv", "w")

    inserts = args.i
    for i in range(inserts):
        key = uuid.uuid4()
        def do_put():
            kv.put(key, randomString())
        duration = timeit.timeit(do_put, number=1)
        output_file.write("%i,%f\n" % (i+1, duration))
        print("inserts %d / %d" % (i, inserts))

    output_file.close()
    oram.close()
