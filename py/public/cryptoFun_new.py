# coding=utf-8
import hashlib

from Crypto.Cipher import AES
import base64

class PrpCrypt(object):
    """
    AES加密与解密
    """
    def __init__(self, key,iv):
        self.key = key
        self.mode = AES.MODE_CBC
        self.cipher_text = None
        self.iv = iv
        self.__BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size

    def get_cryptor(self):
      #  sha384 = hashlisha384b.sha384()
      #  sha384.update(self.key.encode('utf-8'))
      #  res = sha384.digest()

      #  crypt_or = AES.new(res[0:32], self.mode, res[32:48])
        crypt_or = AES.new(self.key.encode(), AES.MODE_CBC, self.iv.encode())
        return crypt_or

    def bytesToHexString(self,bs):
        '''
        bytes转16进制
        '''
        return ''.join(['%02X ' % b for b in bs])

    def hexStringTobytes(self,str):
        '''
       16进制转bytes
       '''
        str = str.replace(" ", "")
        return bytes.fromhex(str)
    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        if not text:
            return text
        cipher = self.get_cryptor()
        decryptByts = self.hexStringTobytes(text)
        msg = cipher.decrypt(decryptByts)
        print(msg)
        print(msg[len(msg) - 1])
        paddingLen = msg[len(msg) - 1]
        return msg[0:-paddingLen]

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cipher = self.get_cryptor()
        x = self.__BLOCK_SIZE_16 - (len(text) % self.__BLOCK_SIZE_16)
        if x != 0:
            text = text + chr(x) * x
        msg = cipher.encrypt(text.encode('utf-8'))
        data = self.bytesToHexString(msg).replace(' ', '')#'\n', ''
        return data
aes_func = PrpCrypt('679LIik$d7De8aDA','rDW1aBLjZ@in^9bm')
