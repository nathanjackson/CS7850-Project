#!/usr/bin/env python3

import random
import string
import sys
import timeit
import uuid

from argparse import ArgumentParser

import pyoram

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store
import privatekv.utils

BLOCK_COUNT = 127 # shoule be 6 levels exactly
BLOCK_SIZE = 4096

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the Path ORAM S3 insertion performance test")
    ap.add_argument("-b", default="test", help="the S3 bucket to use")
    ap.add_argument("-i", default=192, type=int, help="number of inserts")
    ap.add_argument("--create", default=False, action="store_true", help="only create the oram")
    args = ap.parse_args()

    if args.create:
        print("Setting up ORAM")
        pyoram.config.SHOW_PROGRESS_BAR = True
        oram = PathORAM.setup("test", BLOCK_SIZE, BLOCK_COUNT, cached_levels=0, storage_type="s3",
                              bucket_name=args.b, ignore_existing=True)
        kv = privatekv.store.KVORAM(oram)

        keys = set()
        inserts = args.i
        for i in range(inserts):
            key = str(uuid.uuid4())
            kv.put(key, randomString())
            keys.add(key)
            print("inserts %d / %d" % (i, inserts))

        keys_file = open("keys", "w")
        for key in list(keys):
            keys_file.write(key + "\n")
        keys_file.close()

        oram.close()
        privatekv.utils.save_oram_client_data(oram)

    else:
        key, stash, position_map = privatekv.utils.read_oram_client_data("test")
        oram = PathORAM("test", stash, position_map, key=key,
                        storage_type="s3", bucket_name=args.b, ignore_lock=True)
        kv = privatekv.store.KVORAM(oram)
   
        keys = set()

        keys_file = open("keys", "r")
        for key in keys_file.readlines():
            keys.add(key.rstrip())
        keys_file.close()
    
        for i in range(len(keys)):
            key = list(keys)[i]
            for j in range(i+1):
                val = kv.get(key)
                print("gets %d / %d" % (j, (i+1)))

        oram.close()
