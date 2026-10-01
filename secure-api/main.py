import os
from fastapi import FastAPI, HTTPException
import bcrypt

app = FastAPI()

LOG_DIR = os.getenv("LOG_DIR", "/var/log/app")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hash")
def hash_password(password: str = "default_secret"):
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        with open(LOG_FILE, "a") as f:
            f.write("Generated hash for a user\n")

        return {"hash": hashed.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
