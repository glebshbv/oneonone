from fastapi import FastAPI
from db.database import engine
from db.models import user
from db.models import message_history
from api import client, admin

user.Base.metadata.create_all(bind=engine)
message_history.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(client.router, prefix="")
app.include_router(admin.router, prefix="/admin")
