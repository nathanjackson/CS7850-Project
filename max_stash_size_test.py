#!/usr/bin/env python3

import random
import string
import timeit
import uuid

from argparse import ArgumentParser

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store
import privatekv.utils

BLOCK_SIZE = 8192

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":
    ap = ArgumentParser(description="runs the Path ORAM bucket load test")
    ap.add_argument("-n", default=2**15, type=int, help="number of hash buckets")
    args = ap.parse_args()

    print("Setting up ORAM")
    oram = PathORAM.setup("test", BLOCK_SIZE, args.n, storage_type="ram",
                          ignore_existing=True, cached_levels=0)
    kv = privatekv.store.KVORAM(oram)
    output_file = open("insert_time_blocks_%d.csv" % (args.n), "w")

    max_stash_size = 0

    inserts = 1000000
    for i in range(inserts):
        key = uuid.uuid4()
        def do_put():
            kv.put(key, randomString())
        duration = timeit.timeit(do_put, number=1)
        output_file.write("%i,%f\n" % (i+1, duration))

        if len(oram.stash) > max_stash_size:
            max_stash_size = len(oram.stash)

        if 0 == i % 1000:
            print("inserts %d / %d, max stash size = %d" % (i, inserts,
                                                            max_stash_size))

    output_file.close()
    oram.close()
