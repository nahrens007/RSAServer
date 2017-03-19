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