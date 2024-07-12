from src.api.auth.hasher import ShaHasher


def get_hash():
    return ShaHasher()