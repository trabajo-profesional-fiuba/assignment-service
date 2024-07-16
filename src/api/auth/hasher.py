import hashlib

class ShaHasher:

    def hash(self, message: str):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf-8'))
        return sha256_hash.hexdigest()

def get_hasher():
    return ShaHasher