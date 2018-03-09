import time
import uuid
import hashlib
import struct
import binascii


class Block:
    def __init__(self, index, timestamp, previous_hash, data):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.hash = self.get_hash()

    def pack(self):
        return struct.pack("<LL", self.index, self.timestamp) + self.previous_hash + self.data

    def get_hash(self):
        return calc_hash(self.pack())


def current_time():
    return int(time.time())


def calc_hash(src):
    return binascii.hexlify(hashlib.sha256(src).digest())


def genesis_block():
    return Block(0, current_time(), calc_hash(uuid.uuid4().bytes), b"Hello, world!")


def reset_blockchain():
    blockchain.clear()
    blockchain.append(genesis_block())


def add(data):
    last_block = blockchain[-1]
    block = Block(last_block.index + 1, current_time(), last_block.hash, data)
    blockchain.append(block)


def verify_next(block):
    if not blockchain:
        return block.index == 0
    last_block = blockchain[-1]
    return block.previous_hash == last_block.hash


blockchain = []
