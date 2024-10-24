import hashlib

class ShaHasher:
    def hash(self, message: str) -> str:
        """
        Usa SHA-256 para encriptar los bytes del message
        Mas informacion del hash en https://en.wikipedia.org/wiki/SHA-2
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode("utf-8"))
        return sha256_hash.hexdigest()


#TODO - Mover todas las dependencias a un mismo .py
def get_hasher():
    """
    Hasher para injeccion de dependencias
    """
    yield ShaHasher()
