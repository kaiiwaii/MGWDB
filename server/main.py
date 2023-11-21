from sanic import Sanic
from sanic.response import json
from sanic_ext import validate
import asyncio, asyncpg
import httpx
import jwt, bcrypt
import time

from os import environ as env
from dotenv import load_dotenv

import models

load_dotenv()

app = Sanic("MVDB")




JWT_SECRET = env['JWT_SECRET']
IGDB_ID = env['IGDB_ID']
IGDB_SECRET = env['IGDB_SECRET']
SALT = env['SALT'].encode()
DB_URL = env["DB_URL"]

def write_token(data: dict):    
    token_bytes = jwt.encode(data, JWT_SECRET, algorithm='HS256')
    return token_bytes.decode("utf-8")

async def refresh_token(app):
    tk = httpx.post(
            f"https://id.twitch.tv/oauth2/token?client_id={IGDB_ID}&client_secret={IGDB_SECRET}&grant_type=client_credentials"
        ).json()
    print(tk)
    app.ctx.igdb_token = tk["access_token"]
    await asyncio.sleep(int(tk["expires_in"]))

app.add_task(refresh_token)

@app.before_server_start
async def setup_db(app):
    app.ctx.pool = await asyncpg.create_pool(DB_URL)
    async with app.ctx.pool.acquire() as con:
        await con.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id BIGSERIAL PRIMARY KEY,
            username varchar(64) NOT NULL, 
            password varchar(128) NOT NULL,
            email varchar(256) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT NOW(),
            review_template TEXT
        );
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY,
            username BIGINT NOT NULL REFERENCES Users(id),
            review TEXT,
            description TEXT,
            hours DECIMAL,
            platform VARCHAR(64)
        );""")


@app.get("/login")
@validate(query=models.LoginRequest)
async def login(request, query: models.LoginRequest):
    
    async with app.ctx.pool.acquire() as con:
        user = await con.fetchrow(
            """
            SELECT id, email, password FROM Users
            WHERE email = $1;
            """, query.email)
        if user:
            if user["password"] == bcrypt.hashpw(query.password.encode(), SALT).decode("utf-8"):
                return json(
                    {"token": write_token({"id": user["id"], "timestamp": time.time()})}
                )
            else:
                return json({"error": "Invalid password"}, status=401)
        else:
            return json({"error": "Username not found"}, status=404)

@app.post("/signup")
@validate(query=models.SignupRequest)
async def signup(request, query: models.LoginRequest):
    password = bcrypt.hashpw(query.password.encode(), SALT).decode("utf-8")

    async with app.ctx.pool.acquire() as con:
        await con.execute('''
        INSERT INTO Users(username, password, email) values ($1, $2, $3);
        ''', query.username, password, query.email)

    return json({}, status=200)
    
@app.get("api/games")
async def get_games_from_api(request):
    tk = request.args.get("token")
    if tk:
        pass
    else:
        return json({"error": "No token"}, status=400)

    try:
        jwt.decode(tk, JWT_SECRET, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401)
    search = request.args.get("search")
    if search:
        res = httpx.request("POST", url="https://api.igdb.com/v4/games", content=f'''search "{search}";
                             f name, genres, cover, first_release_date, platforms, url;
                             '''
                            , headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})
    return json(res.json())

#REMEMBER: where id = (4356,189,444); (need to test multiple games on one request)
# @app.get("/games")
# @validate(query=models.TokenReq)
# async def get_games(request, query: models.TokenReq):
#     try:
#         userid = jwt.decode(query.token, JWT_SECRET, algorithms=['HS256'])
#         return json(dict(await models.User.filter(id=userid).values("games")), status=200) #well have to test this
    
#     except jwt.exceptions.DecodeError:
#         return json({"error": "Invalid token"}, status=401, dumps=dumps)
    

# @app.post("/addgames")
# @validate(query=models.TokenReq)
# async def add_games(request, query: models.TokenReq, id):
#     try:
#         id = int(id)
#         await models.Game.create(id=id)

#     except:
#         return json({"error": "Invalid ID"}, status=400, dumps=dumps)

#@app.post("get_games")
#

if __name__ == "__main__":
    app.run(port=4321)