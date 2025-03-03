from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import settings

from storage import my_storage
from database import engine
from sqladmin import Admin
from admin import UserAdmin, MaterialAdmin, TopicBlockAdmin, FeedbackAdmin, LearningClassAdmin, StudentClassAdmin
from router import router
from uuid import uuid4


app = FastAPI()

app.mount('/files', StaticFiles(directory='../files'), name='files')


@app.post('/upload/')
async def upload_file(file: UploadFile):
    filename = f'{uuid4()}.{file.filename.split(".")[-1]}'
    path = my_storage.get_path(filename)

    await file.seek(0)
    with open(path, 'wb') as output:
        while True:
            chunk = await file.read(my_storage.default_chunk_size)
            if not chunk:
                break
            output.write(chunk)

    return {'url': f'/files/{filename}'}


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(MaterialAdmin)
admin.add_view(TopicBlockAdmin)
admin.add_view(FeedbackAdmin)
admin.add_view(LearningClassAdmin)
admin.add_view(StudentClassAdmin)

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
    )
