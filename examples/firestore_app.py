import firebase_admin
from fastapi import FastAPI, Request
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.firestore import FirestoreBackend
from fastapi_simple_cache.decorator import cache
from firebase_admin import firestore, credentials

app = FastAPI()


@app.on_event("startup")
async def startup():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'projectId': "sebustam"})
    db = firestore.client()
    collection = db.collection("test_cache")
    backend = FirestoreBackend(collection=collection)
    FastAPISimpleCache.init(backend=backend)
    pass

@app.post("/")
@cache(expire=10)
def root(message: str, request: Request):
    return {"message": message}
