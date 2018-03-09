#!/usr/bin/env python3

import sys
import json
from optparse import OptionParser

from simplechain import *


def read_from_file(filename):
    try:
        with open(filename) as f:
            raw_blocks = json.load(f)
            for raw_block in raw_blocks:
                block = dict_to_block(raw_block)
                if block and verify_next(block):
                    blockchain.append(block)
                else:
                    blockchain.clear()
                    break
    except (IOError, json.JSONDecodeError):
        pass
    if not blockchain:
        reset_blockchain()


def save_to_file(filename):
    with open(filename, "w") as f:
        json.dump([block_to_dict(block) for block in blockchain], f, indent=4)


def read_from_input():
    while True:
        raw_data = sys.stdin.readline().strip()
        if not raw_data:
            break
        add(bytes(raw_data, "utf-8"))


def block_to_dict(block):
    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "previous_hash": block.previous_hash.decode("utf-8"),
        "data": block.data.decode("utf-8"),
        "hash": block.hash.decode("utf-8")
    }


def dict_to_block(raw_block):
    index = int(raw_block["index"])
    timestamp = int(raw_block["timestamp"])
    previous_hash = bytes(raw_block["previous_hash"], "utf-8")
    data = bytes(raw_block["data"], "utf-8")
    block = Block(index, timestamp, previous_hash, data)
    block_hash = bytes(raw_block["hash"], "utf-8")
    if block.hash != block_hash:
        return None
    return block


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", metavar="FILE",
                      help="write output to FILE",
                      default="blockchain.json")
    (options, args) = parser.parse_args()

    read_from_file(options.filename)
    read_from_input()
    save_to_file(options.filename)


if __name__ == "__main__":
    main()
