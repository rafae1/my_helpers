import base64
import zlib

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, MD5


class InvalidSignature(Exception):
    pass


def encrypt(plain_str: str, key: bytes) -> bytes:
    """
    Шифрование AES.MODE_CBC с подписью
    Структура ответа: iv(16B) + encrypted + sign(16B)
    """
    iv = Random.new().read(AES.block_size)  # initial value
    aes = AES.new(key, AES.MODE_CBC, iv)
    message = iv + aes.encrypt(_pkcs7_pad(zlib.compress(plain_str.encode())))
    sign = make_sign(message, key)
    return base64.b64encode(message + sign)


def decrypt(encrypted_bytes, key, with_sign=True):
    decrypted = base64.decodebytes(encrypted_bytes)
    if with_sign:
        sign = decrypted[-MD5.digest_size:]
        decrypted = decrypted[:-MD5.digest_size]
        actual_sign = make_sign(decrypted, key)
        if sign != actual_sign:
            raise InvalidSignature

    iv = decrypted[:AES.block_size]
    msg = decrypted[AES.block_size:]
    return zlib.decompress(
        _pkcs7_unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(msg))).decode()


def make_sign(message, key):
    return HMAC.new(key, msg=message, digestmod=MD5).digest()


def encrypt_ecb(plain_str, key, encode=base64.b64encode):
    """ Зашифровать строку plain_str ключем key и закодировать в текст функцией encode"""
    return encode(AES.new(key).encrypt(
        _pkcs7_pad(zlib.compress(plain_str.encode())))).decode()


def decrypt_ecb(encrypted_str, key, decode=base64.decodebytes):
    """ Расшифровать строку encrypted_str ключем key и РАскодировав её из текста функцией decode"""
    return zlib.decompress(_pkcs7_unpad(
        AES.new(key).decrypt(decode(encrypted_str.encode())))).decode()


def _pkcs7_pad(text):
    val = AES.block_size - (len(text) % AES.block_size)
    return text + str.encode(chr(val) * val)


def _pkcs7_unpad(text):
    return text[:-text[-1]]
