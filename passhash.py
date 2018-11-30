import hashlib

print('変換したい文字列を入力')
id = input()
id = hashlib.sha256(id.encode('utf-8')).hexdigest()
print(id)