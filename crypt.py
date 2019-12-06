from Crypto.Cipher import AES
import config

key = config.crypto_key
mode = AES.MODE_CBC
iv = key

def encrypt(text):#加密
    text = text.encode('utf-8')
    lenth = 16
    if len(text) < lenth:
        add = lenth-len(text)
        text = text + ('\0' * add).encode('utf-8')
    elif len(text) > lenth:
        add = lenth-(len(text) % lenth)
        text = text + ('\0' * add).encode('utf-8')
    cryptor = AES.new(key.encode('utf-8'),mode,iv.encode('utf-8'))
    ans = cryptor.encrypt(text)
    return ans

def decrypt(x):#解密
    cryptor = AES.new(key.encode('utf-8'),mode,iv.encode('utf-8'))
    plain_text = cryptor.decrypt(x)
    return plain_text.decode('utf-8').rstrip('\0')


if __name__ == '__main__':
    text = '你好'
    x = encrypt(text)
    print(x)
    b = decrypt(x)
    print(b)
