#!/usr/bin/env python3

import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..")))

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store
import privatekv.utils

BLOCK_SIZE = 4096
BLOCK_COUNT = 2 ** (8 + 1) - 1

class TestKVORAM(unittest.TestCase):
    def setUp(self):
        self.oram = PathORAM.setup("test", BLOCK_SIZE, BLOCK_COUNT,
                                   storage_type="ram", ignore_existing=True)
        self.store = privatekv.store.KVORAM(self.oram)

    def tearDown(self):
        self.oram.close()

    def test_simple_put_get(self):
        self.store.put("foobar", 3)
        self.assertEqual(self.store.get("foobar"), 3)
        self.store.put(3, "foobar")
        self.assertEqual(self.store.get(3), "foobar")
        self.assertNotEqual(self.store.get(3), self.store.get("foobar"))

    def test_collision_resolution(self):
        # for collision resolution: hash(3) % 511 == hash(514) % 511
        self.store.put(3, "foobar")
        self.store.put(514, "bazbar")
        self.assertNotEqual(self.store.get(3), self.store.get(514))

    def test_non_existent_key(self):
        self.assertRaises(privatekv.store.KeyNotFoundError, self.store.get,
                          "thisdoesnotexist")
        self.assertRaises(privatekv.store.KeyNotFoundError, self.store.get, 3)

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_save_client_data(self):
        oram = PathORAM.setup(os.path.join(self.tmpdir.name, "test"), BLOCK_SIZE,
                              BLOCK_COUNT, storage_type="file",
                              ignore_existing=True)
        data = b"hello world"
        data += b"\x00" * (oram.block_size - len(data))
        oram.write_block(0, bytes(data))
        oram.close()
        privatekv.utils.save_oram_client_data(oram, path=self.tmpdir.name)

        key, stash, pm = privatekv.utils.read_oram_client_data("test",
                                                               path=self.tmpdir.name)
        oram = PathORAM(os.path.join(self.tmpdir.name, "test"), stash, pm, key=key,
                        storage_type="file")
        self.assertEqual(data, oram.read_block(0))
        oram.close()

    def test_compute_level_load(self):
        oram = PathORAM.setup("test", 32, 1, bucket_capacity=1,
                              storage_type="ram", ignore_existing=True,
                              cached_levels=0)
        result = privatekv.utils.compute_avg_level_load(oram)
        self.assertEqual(1.0, result[0])
        oram.close()

if __name__ == "__main__":
    unittest.main()
