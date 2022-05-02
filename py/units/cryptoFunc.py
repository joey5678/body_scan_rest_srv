# coding=utf-8

from Crypto.Cipher import DES
import base64


mdes = DES.new(b'fnd12)I&', 1)


def decode_base64(text):
    if not text: return text
    data = text.encode("utf-8")
    ret = mdes.decrypt(base64.decodebytes(data))
    padding_len = ret[-1]
    dec_text = ret[:-padding_len].decode("utf-8")
    return dec_text


def encrypt_base64(text):
    pad_len = 8 - len(text) % 8
    padding = chr(pad_len) * pad_len
    text += padding

    data = text.encode("utf-8")
    data = base64.encodebytes(mdes.encrypt(data))
    return data.decode("utf-8").replace('\n', '')


if __name__ == '__main__':
    aa = encrypt_base64("12345678")
    print(aa)
    enc_t = decode_base64(aa)
    print(enc_t)
