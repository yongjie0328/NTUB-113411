import uvicorn
from backend_server import app as application

if __name__ == "__main__":
    uvicorn.run("backend_server:app", host="192.168.120.30", port=1234, reload=True)
