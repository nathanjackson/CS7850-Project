#!/usr/bin/env python3

import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..")))

from pyoram.oblivious_storage.tree.path_oram import PathORAM

import privatekv.store

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

if __name__ == "__main__":
    unittest.main()
