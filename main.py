import uvicorn  # type: ignore

from config.settings import PORT
from config.settings import DEBUG

if __name__ == "__main__":
    uvicorn.run('app:app',
                host='0.0.0.0',
                port=PORT,
                reload=DEBUG)
