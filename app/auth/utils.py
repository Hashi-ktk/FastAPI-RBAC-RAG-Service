from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt_token(data: dict, secret: str, algorithm: str = "HS256") -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)
    data.update({"exp": expiration})
    token = jwt.encode(data, secret, algorithm=algorithm)
    return token

def verify_jwt_token(token: str, secret: str, algorithm: str = "HS256") -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    
def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)