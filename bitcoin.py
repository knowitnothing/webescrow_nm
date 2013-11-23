#
# Note: Thiw will generate uncompressed keys.
#

import ecdsa
import hashlib
from OpenSSL import rand

BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
NETWORK_ID = '\x00' # Main Network
ADDR_PREFIX = '1' # Bitcoin pubkey.

MAX_KEY = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def privatekey():
    # See https://en.bitcoin.it/wiki/Private_key
    int_pk = 0
    while not (int_pk > 0 and int_pk <= MAX_KEY): # :)
        pk = hashlib.sha256(rand.bytes(32))
        int_pk = int(pk.hexdigest(), 16)
    return int_pk, wif(pk.digest())

def wif(privkey):
    # See https://en.bitcoin.it/wiki/Wallet_import_format
    ext = b'\x80' + privkey
    key_ext = hashlib.sha256(hashlib.sha256(ext).digest())
    bin_addr = ext + key_ext.digest()[:4]
    return to_base58(bin_addr)

def address(privkey):
    # See https://en.bitcoin.it/wiki/Technical_background_of_Bitcoin_addresses
    pub_key = ecdsa.SigningKey.from_secret_exponent(privkey,
            ecdsa.curves.SECP256k1).get_verifying_key().to_string()
    pub_key_hash = hashlib.sha256(b'\x04' + pub_key).digest()
    pub_key_ripe = NETWORK_ID + hashlib.new('ripemd160', pub_key_hash).digest()
    pub_key_ext = hashlib.sha256(hashlib.sha256(pub_key_ripe).digest())

    bin_addr = pub_key_ripe + pub_key_ext.digest()[:4]

    address = to_base58(bin_addr)
    return ADDR_PREFIX + address

def to_base58(b):
    pubnum = int(b.encode('hex'), 16)
    dec = ''
    while pubnum:
        pubnum, rem = divmod(pubnum, 58)
        dec = BASE58[rem] + dec
    return dec

