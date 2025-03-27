from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from router import router


app = FastAPI()

origins = [
    settings.main.url
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
