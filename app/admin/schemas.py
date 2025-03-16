from pydantic import BaseModel
from typing import List, Optional

class AdminCreate(BaseModel):
    username: str
    password: str
    email: str

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

class AdminInDB(BaseModel):
    id: int
    username: str
    email: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permissions: Optional[List[str]] = None

class RoleInDB(BaseModel):
    id: int
    name: str
    permissions: List[str]

class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: List[str]