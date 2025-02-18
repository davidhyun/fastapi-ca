from passlib.context import CryptContext

class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    def encrypt(self, secret):
        return self.pwd_context.hash(secret)
    
    def verify(self, secret, hash):
        # secret: 사용자가 입력한 비밀번호 (평문)
        # hash: 데이터베이스에 저장된 비밀번호 (암호화)
        return self.pwd_context.verify(secret, hash)