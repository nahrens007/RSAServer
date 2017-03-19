import rsa

(pub, priv) = rsa.newkeys(1024) #generate 1024 bit key pair
msg = "HELLO WORLD"

encrypted = rsa.encrypt(msg.encode(), pub)
print("encrypted: ", encrypted)
decrypted = rsa.decrypt(encrypted, priv)
print("decrypted: ", decrypted)
pub_pem = pub.save_pkcs1()
priv_pem = priv.save_pkcs1()
print('pub: ', pub_pem)
print('priv: ', priv_pem)

print()
print('pub loaded: ', rsa.key.PublicKey.load_pkcs1(pub_pem, 'PEM'))
print('pub loaded: ', rsa.key.PrivateKey.load_pkcs1(priv_pem, 'PEM'))

a_key = '-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAL3PtrjCa1Zdnn8LT75TbXe8uWLzDjxx6bSUgIgfYvCXFsVCOe9KtOUA\nP3ZXBEQtxcSuX4n0vSStIKtyhcou5/MaY9h6wbJ0PBykyYEZZwG2vkclCF2pfEWh\neiY4AIMyT+R+ubUX3LCCphJ/1dDgVCq2da6k0A6K2/f6iFysHk3LAgMBAAE=\n-----END RSA PUBLIC KEY-----\n'
ano = rsa.key.PublicKey.load_pkcs1(a_key, 'PEM')
print(ano)

print("Hello world!\r".strip('\r\n')) #string can have just \r or \n, it will still strip

