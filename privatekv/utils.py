import os
import pickle
import struct

from pyoram.oblivious_storage.tree.tree_oram_helper import TreeORAMStorage
from pyoram.util.virtual_heap import calculate_bucket_level
from pyoram.encrypted_storage.top_cached_encrypted_heap_storage import TopCachedEncryptedHeapStorage

def save_oram_client_data(oram, path=os.path.curdir):
    """
    Saves an ORAM's client side data to the specified directory.
    :oram: The ORAM object to save
    :path: The path to save (defaults to current directory)
    """
    store_name = oram._oram.storage_heap.storage_name
    key_file_name = "%s.key" % (store_name)
    stash_file_name = "%s.stash" % (store_name)
    pos_file_name = "%s.position" % (store_name)
    with open(os.path.join(path, key_file_name), "wb") as kf:
        kf.write(oram.key)
    with open(os.path.join(path, stash_file_name), "wb") as sf:
        pickle.dump(oram.stash, sf)
    with open(os.path.join(path, pos_file_name), "wb") as pf:
        pickle.dump(oram.position_map, pf)

def read_oram_client_data(store_name, path=os.path.curdir):
    """
    Reads an ORAM's client side data from the specified directory.
    :store_name: The store name to use
    :path: The path to load from (defaults to current directory).
    """
    key_file_name = "%s.key" % (store_name)
    stash_file_name = "%s.stash" % (store_name)
    pos_file_name = "%s.position" % (store_name)
    with open(os.path.join(path, key_file_name), "rb") as kf:
        key = kf.read()
    with open(os.path.join(path, stash_file_name), "rb") as sf:
        stash = pickle.load(sf)
    with open(os.path.join(path, pos_file_name), "rb") as pf:
        position_map = pickle.load(pf)
    return key, stash, position_map

def compute_avg_level_load(oram):
    """
    Returns the average bucket load for each level in a Path ORAM. This
    function is incompatible with caching. To use this function, your ORAM must
    have been initialized with the cached_levels=0 argument.
    :oram: The Path ORAM to use
    """
    assert type(oram.heap_storage) != TopCachedEncryptedHeapStorage
    level_blocks_inuse = {}
    level_blocks_total = {}
    # for each bucket id
    for bucket in range(oram.heap_storage.virtual_heap.bucket_count()):
        # get the bucket level
        level = calculate_bucket_level(oram.heap_storage.virtual_heap.k, bucket)
        # add level to the map if this is the first time we've seen it
        if level not in level_blocks_inuse:
            level_blocks_inuse[level] = 0
        if level not in level_blocks_total:
            level_blocks_total[level] = 0
        # read the bucket from bucket storage
        bucket_data = oram.heap_storage.bucket_storage.read_block(bucket)
        # compute block parameters
        block_info_fmt = TreeORAMStorage.block_info_storage_string
        block_info_size = struct.calcsize(block_info_fmt)
        block_size = oram.block_size + block_info_size
        # now extract the block info for each bucket
        for block in range(oram.heap_storage.blocks_per_bucket):
            start = block * block_size
            block_info_data = bucket_data[start:start+block_info_size]
            (real_block, block_id) = struct.unpack(block_info_fmt, block_info_data)
            level_blocks_total[level] += 1
            if True == real_block:
                level_blocks_inuse[level] += 1
    # compute percentages
    level_percent_inuse = {}
    for level, total in level_blocks_total.items():
        level_percent_inuse[level] = float(level_blocks_inuse[level]) / float(total)
    return level_percent_inuse
