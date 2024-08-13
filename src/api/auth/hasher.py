import hashlib


class ShaHasher:
    def hash(self, message: str) -> str:
        """Uses SHA256 to create a hash of the message
        and return it in hexa as string.
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode("utf-8"))
        return sha256_hash.hexdigest()


def get_hasher():
    """
    For dependency injection
    """
    yield ShaHasher()
