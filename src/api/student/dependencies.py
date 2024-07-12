from src.api.auth.hasher import ShaHasher
from src.config.database import Database


def get_hash():
    return ShaHasher()


def get_db():
    return Database()