#!/usr/bin/env python3

import random
import string

from argparse import ArgumentParser

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store
import privatekv.utils

BLOCK_SIZE = 4096
#BLOCK_COUNT = 2 ** (8 + 1) - 1
BLOCK_COUNT = 2**15

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the PrivateKV bucket load test")
    ap.add_argument("-z", default=4, type=int, help="number of blocks in a bucket")
    args = ap.parse_args()

    print("Setting up ORAM")
    oram = PathORAM.setup("test", BLOCK_SIZE, BLOCK_COUNT, storage_type="ram",
                          ignore_existing=True, cached_levels=0,
                          bucket_capacity=args.z)
    kv = privatekv.store.KVORAM(oram)

    n = 1000000
    for i in range(n):
        key = random.randint(0, 100000)
        kv.put(key, randomString())

        if 0 == i % 1000:
            print("inserts %d / %d" % (i, n))

    print("computing level loads")
    loads = privatekv.utils.compute_avg_level_load(oram)
    print("level,load")
    for level in sorted(loads.keys()):
        print("%d,%f" % (level, loads[level]))

    oram.close()
