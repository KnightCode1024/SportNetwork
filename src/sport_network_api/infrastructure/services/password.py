import bcrypt


class PasswordService:    
    def __init__(self, rounds: int = 12):
        self.rounds = rounds
    
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.rounds)
        pwd_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_bytes.decode("utf-8")
    
    def verify(self, password: str, password_hash: str) -> bool:
        pwd_bytes = password.encode("utf-8")
        hash_bytes = password_hash.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
