from sanic import Sanic
from sanic.response import json
from sanic_ext import validate, Extend
from sanic_cors import CORS
import asyncio, asyncpg
import httpx
import jwt, bcrypt
import time
import datetime

from os import environ as env
from dotenv import load_dotenv

import models

load_dotenv()

app = Sanic("MGWDB")
# CORS_OPTIONS = {"resources": r"/*", "origins": ["http://localhost:5173/"], "supports_credentials": True, "methods": ["POST, GET, OPTIONS"]}
# Extend(app, extensions=[CORS], config={"CORS": False, "CORS_OPTIONS": CORS_OPTIONS})

JWT_SECRET = env['JWT_SECRET']
IGDB_ID = env['IGDB_ID']
IGDB_SECRET = env['IGDB_SECRET']
SALT = env['SALT'].encode()
DB_URL = env["DB_URL"]

def write_token(data: dict):    
    token_bytes = jwt.encode(data, JWT_SECRET, algorithm='HS256')
    return token_bytes.decode("utf-8")

@app.middleware('response')
async def add_cors_headers(request, response):
    response.headers['Access-Control-Allow-Headers'] = 'access-control-allow-origin'
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5173'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods']='POST, OPTIONS, GET'


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
            review_template VARCHAR(4096)
        );
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY,
            username BIGINT NOT NULL REFERENCES Users(id),
            review VARCHAR(4096),
            description VARCHAR(4096),
            hours DECIMAL,
            played_platform smallint[2]
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
                r = json({})
                tk = write_token({"id": user["id"], "timestamp": time.time()})
                r.add_cookie("token", tk, samesite="None", expires=datetime.datetime.now() + datetime.timedelta(days=7), path=r"/*")
                return r
            else:
                return json({"error": "Invalid password"}, status=401)
        else:
            return json({"error": "Email not found"}, status=404)

@app.post("/signup")
@validate(query=models.SignupRequest)
async def signup(request, query: models.SignupRequest):
    password = bcrypt.hashpw(query.password.encode(), SALT).decode("utf-8")

    async with app.ctx.pool.acquire() as con:
        await con.execute('''
        INSERT INTO Users(username, password, email) values ($1, $2, $3);
        ''', query.username, password, query.email)

    return json({}, status=200)
    
@app.get("api/searchgames")
async def search_games_from_api(request):
    try:
        jwt.decode(request.cookies.get("token"), JWT_SECRET, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401)
    
    search = request.args.get("search")
    if search:
        async with httpx.AsyncClient() as c:
            res = await c.request("POST", url="https://api.igdb.com/v4/games", content=f'''search "{search}";
                             f name, genres.name, cover.image_id, first_release_date, platforms.abbreviation, url;
                             '''
                            , headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})
            return json(res.json())
    else:
        return json({"error": "Please add a search term"}, status=400)

#REMEMBER: where id = (4356,189,444); (need to test multiple games on one request)
# @app.get("/games")
# @validate(query=models.TokenReq)
# async def get_games(request, query: models.TokenReq):
#     try:
#         userid = jwt.decode(query.token, JWT_SECRET, algorithms=['HS256'])
#         return json(dict(await models.User.filter(id=userid).values("games")), status=200) #well have to test this
    
#     except jwt.exceptions.DecodeError:
#         return json({"error": "Invalid token"}, status=401, dumps=dumps)
    

@app.post("/addgames")
async def add_games(request):
    body = request.json
    if body:
        try:
            userid = jwt.decode(request.cookies.get("token"), JWT_SECRET, algorithms=['HS256'])["id"]
            async with app.ctx.pool.acquire() as con:
                await con.executemany(
                    '''
                    INSERT INTO Games (id, username, review, description, hours, played_platform)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ''',
                    [(row['id'], userid, row.get('review', ""), row.get('description', ""), row.get('hours', 0), row.get('played_platform', [])) for row in body]
                )
            
        except jwt.exceptions.DecodeError:
            return json({"error": "Invalid token"}, status=401)
        
    return json({"error": "No body"}, status=400)


@app.get("mygames")
async def get_games(request):
    try:
        userid = jwt.decode(request.cookies.get("token"), JWT_SECRET, algorithms=['HS256'])["id"]
        db_games = []
        async with app.ctx.pool.acquire() as con:
            rows = await con.fetch("SELECT id, review, description, hours, played_platform from Games where username = $1", userid)
            db_games = [{"id":str(row["id"]), "review":row.get('review'), "description":row.get('description'),"hours":row.get('hours'), "played_platform":row.get('played_platform')} for row in rows]
        

        if len(db_games) > 0:
            data = []
            async with httpx.AsyncClient() as c:
                res = await c.request("POST", url="https://api.igdb.com/v4/games", content=f'''f name, genres.name, cover.image_id, first_release_date,platforms.abbreviation, url; where id = ({",".join([str(g["id"]) for g in db_games])});
                    '''
                ,headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})
                data = res.json()

            merged_games = []
            for game_info in data:
                api_id = str(game_info["id"])
                del game_info["id"]
                matching_game = next((g for g in db_games if str(g["id"]) == api_id), None)
                
                if matching_game:
                    # Create a new dictionary with the updated values
                    updated_game = matching_game.copy()
                    updated_game.update(game_info)
                    merged_games.append(updated_game)
                else:
                    # If the ID is not found in db_games, add the original dictionary from data
                    merged_games.append(game_info)     

            return json(merged_games)

            

    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=4321, debug=True)
