from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(title="Auth Demo API")

# Security scheme
security = HTTPBearer()

# Protected endpoint
@app.get("/secure")
def secure_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {
        "token_type": credentials.scheme,
        "token": credentials.credentials
    }

# Public endpoint
@app.get("/")
def public():
    return {"msg": "Public endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
