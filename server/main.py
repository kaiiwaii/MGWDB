from sanic import Sanic
from sanic.response import json
from sanic_ext import validate
from sanic_motor import BaseModel
from orjson import dumps
import httpx
import jwt, bcrypt


from os import environ as env
from dotenv import load_dotenv

import models
from models import User

load_dotenv()

app = Sanic("MVDB")

settings = dict(
    MOTOR_URI='mongodb://localhost:27017/mvdb', LOGO=None
)
app.config.update(settings)

BaseModel.init_app(app)

JWT_SECRET = env['JWT_SECRET']
IGDB_ID = env['IGDB_ID']
IGDB_SECRET = env['IGDB_SECRET']
SALT = env['SALT'].encode()

def write_token(payload: dict):    
    token_bytes = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token_bytes.decode("utf-8")
    

@app.get("/login")
@validate(query=models.LoginRequest)
async def login(request, query: models.LoginRequest):
    user = await User.find_one()
    if user and user.password == query.password:

        tk = httpx.post(
            f"https://id.twitch.tv/oauth2/token?client_id={IGDB_ID}&client_secret={IGDB_SECRET}&grant_type=client_credentials"
        ).json()
        
        return json({"mvdb_token": write_token({"id": user.id}),"igdb_token": tk["access_token"]}, status=200, dumps=dumps)
    
@app.post("/signup")
@validate(query=models.SignupRequest)
async def signup(request, query: models.LoginRequest):
    user = User(username=query.username, 
             email=query.email, 
             password=bcrypt.hashpw(query.password.encode(), SALT).decode("utf-8")
            )
    if await user.is_unique():
        await User.insert_one(user.__dict__)
    else:
        return json({"error": "Username or email are already taken"}, status=400, dumps=dumps)
    return json({}, status=200, dumps=dumps)


@app.get("/games")
@validate(query=models.TokenReq)
async def get_games(request, query: models.TokenReq):
    try:
        userid = jwt.decode(query.token, JWT_SECRET, algorithms=['HS256'])
        return json(dict(await models.User.filter(id=userid).values("games")), status=200) #well have to test this
    
    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401, dumps=dumps)

@app.post("/addgames")
@validate(query=models.TokenReq)
async def add_games(request, query: models.TokenReq, id):
    try:
        id = int(id)
        await models.Game.create(id=id)

    except:
        return json({"error": "Invalid ID"}, status=400, dumps=dumps)


if __name__ == "__main__":
    app.run(port=4321)