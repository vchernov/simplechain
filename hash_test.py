#!/usr/bin/env python3

import hashlib
import struct
import binascii


class Header:
    def __init__(self):
        self.version = 1
        self.previous_block = b""
        self.merkle_root = b""
        self.timestamp = 0
        self.bits = 0
        self.nonce = 0

    def pack(self):
        return (struct.pack('<L', self.version) +
                binascii.unhexlify(self.previous_block)[::-1] +
                binascii.unhexlify(self.merkle_root)[::-1] +
                struct.pack('<LLL', self.timestamp, self.bits, self.nonce))

    def get_hash(self):
        return hashlib.sha256(hashlib.sha256(self.pack()).digest()).digest()


def run_test():
    header = Header()
    header.previous_block = b"00000000000008a3a41b85b8b29ad444def299fee21793cd8b9e567eab02cd81"
    header.merkle_root = b"2b12fcf1b09288fcaff797d71e950e71ae42b91e8bdb2304758dfcffc2b620e3"
    header.timestamp = 1305998791
    header.bits = 440711666
    header.nonce = 2504433986
    print(binascii.hexlify(header.get_hash()[::-1]))


def run_example():
    header_hex = binascii.unhexlify(b"01000000" +
                                    b"81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000" +
                                    b"e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b" +
                                    b"c7f5d74d" +
                                    b"f2b9441a" +
                                    b"42a14695")
    final_hash = hashlib.sha256(hashlib.sha256(header_hex).digest()).digest()
    print(binascii.hexlify(final_hash[::-1]))


if __name__ == "__main__":
    run_example()
    run_test()
