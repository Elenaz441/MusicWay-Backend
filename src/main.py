from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from logger import log_config
from admin.admin import setup_admin
from storage import my_storage
from router import router
from uuid import uuid4


app = FastAPI()
setup_admin(app)


@app.post('/upload/')
async def upload_file(file: UploadFile):
    filename = f'materials-{uuid4()}.{file.filename.split(".")[-1]}'
    await file.seek(0)
    my_storage.write(file.file, filename)
    file_url = my_storage.get_path(filename)
    return {'url': file_url}


origins = [
    settings.front.url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
                   'Authorization'],
)

app.include_router(router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=log_config
    )
