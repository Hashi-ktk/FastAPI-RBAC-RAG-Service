import os 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.admin.routes import router as admin_router
from app.rbac.oso import initialize_oso

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
async def startup_event():
    initialize_oso()  # Initialize Oso and load policies
    os.makedirs("workspace", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI RBAC Microservice"}