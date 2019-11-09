#!/usr/bin/env python3

import pickle

import paramiko

from pyoram.oblivious_storage.tree.path_oram import PathORAM

class KeyNotFoundError(Exception):
    """Raised whenever a key was not found in a KV Store."""
    def __init__(self, key):
        self.key = key
        super(KeyNotFoundError, self).__init__("Key \"%s\" not found" % (key))

class KVORAM(object):
    """
    KVORAM objects wrap a PathORAM object. KVORAM acts as an abstraction layer
    to provide the user with an easy to use key-value inteface.
    """
    def __init__(self, oram):
        """
        Setup a PathORAM backend given the PathORAM object.
        :oram: the ORAM object
        """
        self.oram = oram

    def put(self, key, val):
        """
        Insert or update a key-value pair into the ORAM.
        :key: the key
        :val: the value
        """
        # First compute the hash of the key and block where the data will be
        # stored.
        h = hash(key)
        block_id = h % self.oram.block_count

        # Next retrieve the hash bucket from ORAM. If not, create a new bucket.
        try:
            bucket = self._get_hash_bucket(block_id)
        except pickle.UnpicklingError as e:
            bucket = {}

        # Insert the key-value pair into the hash bucket.
        bucket[key] = val

        # Write the bucket back to ORAM
        self._write_hash_bucket(block_id, bucket)

    def _get_hash_bucket(self, block_id):
        data = self.oram.read_block(block_id)
        return pickle.loads(data)

    def _write_hash_bucket(self, block_id, bucket):
        pickled = pickle.dumps(bucket)
        assert len(pickled) <= self.oram.block_size
        pickled += b"\x00" * (self.oram.block_size - len(pickled))
        self.oram.write_block(block_id, bytes(pickled))

    def get(self, key):
        """
        Retrieves the value for the given key from ORAM.
        :key: the key
        """
        # Compute the hash of the key and block where to look for data.
        h = hash(key)
        block_id = h % self.oram.block_count

        # Read the data from the block.
        data = self.oram.read_block(block_id)
        # Attempt to deserialize.
        try:
            bucket = pickle.loads(data)
            return bucket[key]
        except pickle.UnpicklingError as e:
            raise KeyNotFoundError(key) from e
