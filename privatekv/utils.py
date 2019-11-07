import os
import pickle

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
