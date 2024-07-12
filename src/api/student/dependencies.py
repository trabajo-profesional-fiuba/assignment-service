from src.api.auth.hasher import SHA1Hasher


def get_hash():
    return SHA1Hasher()