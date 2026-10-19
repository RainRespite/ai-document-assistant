import hashlib
text1 = "Python"
text2 = "Python "
hash1 = hashlib.sha256(text1.rstrip().encode("utf-8")).hexdigest()
hash2 = hashlib.sha256(text2.rstrip().encode("utf-8")).hexdigest()

print(hash1 == hash2)