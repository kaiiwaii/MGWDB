from sanic import Sanic
from sanic.response import json
from sanic_ext import validate, Extend
import asyncio
import asyncpg
import httpx
import jwt
import bcrypt
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
CODE_SECRET = env['CODE_SECRET']

def write_token(data: dict):
    token_bytes = jwt.encode(data, JWT_SECRET, algorithm='HS256')
    try:
        return token_bytes.decode("utf-8")
    except:
        return token_bytes


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


@app.middleware('response')
async def add_cors_headers(request, response):
    response.headers['Access-Control-Allow-Headers'] = 'access-control-allow-origin'
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5173'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'


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
            review_template VARCHAR(4096),
            is_public BOOLEAN DEFAULT FALSE
        );
        CREATE TABLE IF NOT EXISTS Games (
            inner_id BIGSERIAL PRIMARY KEY,
            id INTEGER,
            username BIGINT NOT NULL REFERENCES Users(id),
            rating VARCHAR(4096) DEFAULT '',
            description VARCHAR(4096) DEFAULT '',
            hours DOUBLE PRECISION DEFAULT 0,
            played_platform INTEGER DEFAULT -1
        );
                          
        CREATE UNIQUE INDEX IF NOT EXISTS games_unique_idx
                ON Games(id, username);
                          
        """)

        # CREATE TABLE IF NOT EXISTS Cache (
        #     id INTEGER PRIMARY KEY,
        #     name TEXT,
        #     genres
        #     f name, genres.name, cover.image_id, first_release_date,platforms.id, platforms.abbreviation, url;
        # )


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
                r = json({"template": user.get("review_template")})
                tk = write_token({"id": user["id"], "timestamp": time.time()})
                r.add_cookie("token", tk, samesite="None", expires=datetime.datetime.now(
                ) + datetime.timedelta(days=7), path="/")
                return r
            else:
                return json({"error": "Invalid password"}, status=401)
        else:
            return json({"error": "Email not found"}, status=404)


@app.post("/signup")
@validate(query=models.SignupRequest)
async def signup(request, query: models.SignupRequest):
    password = bcrypt.hashpw(query.password.encode(), SALT).decode("utf-8")
    try:
        jwt.decode(query.code, CODE_SECRET, algorithms=['HS256'])
    except:
        return json({"error": "Invalid code"}, status=401)
    async with app.ctx.pool.acquire() as con:
        await con.execute('''
        INSERT INTO Users(username, password, email) values ($1, $2, $3);
        ''', query.username, password, query.email)

    return json({}, status=200)


@app.get("api/searchgames")
async def search_games_from_api(request):
    try:
        jwt.decode(request.cookies.get("token"),
                   JWT_SECRET, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401)

    search = request.args.get("search")
    if search:
        async with httpx.AsyncClient() as c:
            res = await c.request("POST", url="https://api.igdb.com/v4/games", content=f'''search "{search}";
                             f name, genres.name, cover.image_id, first_release_date, platforms.id, platforms.abbreviation, url; limit 20;
                             ''', headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})
            return json(res.json())
    else:
        return json({"error": "Please add a search term"}, status=400)

# REMEMBER: where id = (4356,189,444); (need to test multiple games on one request)
# @app.get("/games")
# @validate(query=models.TokenReq)
# async def get_games(request, query: models.TokenReq):
#     try:
#         userid = jwt.decode(query.token, JWT_SECRET, algorithms=['HS256'])
#         return json(dict(await models.User.filter(id=userid).values("games")), status=200) #well have to test this

#     except jwt.exceptions.DecodeError:
#         return json({"error": "Invalid token"}, status=401, dumps=dumps)


@app.post("addtemplate")
async def add_template(request):
    body = request.json
    if body:
        template = body.get("template")
        if not template:
            return json({"error": "No template"})
        try:
            userid = jwt.decode(request.cookies.get(
                "token"), JWT_SECRET, algorithms=['HS256'])["id"]
            async with app.ctx.pool.acquire() as con:
                await con.execute(
                    '''
                    UPDATE Users SET review_template = $1 WHERE id=$2
                    ''',
                    template, int(userid)
                )
                return json({}, status=200)

        except jwt.exceptions.DecodeError:
            return json({"error": "Invalid token"}, status=401)
    else:
        return json({"error": "No body"}, status=400)


@app.post("/addgames")
async def add_games(request):
    body = request.json

    if body:
        try:
            userid = jwt.decode(request.cookies.get(
                "token"), JWT_SECRET, algorithms=['HS256'])["id"]
            async with app.ctx.pool.acquire() as con:
                await con.executemany(
                    '''
                    INSERT INTO Games (id, username, rating, description, hours, played_platform)
                    VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT(id, username) DO UPDATE SET rating=$3, description=$4, hours=$5, played_platform=$6
                    ''',
                    [(row['id'], userid, row.get('rating', ""), row.get('description', ""), row.get(
                        'hours', 0), int(row.get('played_platform', -1))) for row in body]
                )
                return json({}, status=200)

        except jwt.exceptions.DecodeError:
            return json({"error": "Invalid token"}, status=401)
    else:
        return json({"error": "No body"}, status=400)


@app.post("/deletegame")
async def delete_games(request):
    id = request.args.get("id")
    if id:
        try:
            userid = jwt.decode(request.cookies.get(
                "token"), JWT_SECRET, algorithms=['HS256'])["id"]
            async with app.ctx.pool.acquire() as con:
                await con.execute(
                    '''
                    DELETE FROM Games where id=$1 and username=$2
                    ''',
                    int(id), userid
                )
                return json({}, status=200)
        except jwt.exceptions.DecodeError:
            return json({"error": "Invalid token"}, status=401)

    return json({"error": "No id"})

@app.get("/user/<username>")
async def get_profile(request, username):
    db_data = []
    async with app.ctx.pool.acquire() as con:
        d = await con.fetchrow("SELECT is_public from Users where username = $1;", username)
        is_public = t.get("is_public")
        if is_public == False:
            return json({"error": "User doesn't exist or doesn't have a public profile"})
        else:
            rows = await con.fetch("SELECT id, rating, description, hours, played_platform from Games where username = $1;", username)
            db_data = [{"id": int(row["id"]), "rating": str(row.get('rating')), "description": row.get(
                'description'), "hours": row.get('hours'), "played_platform": row.get('played_platform')} for row in rows]

            if len(db_data) > 0:
                api_data = []
                async with httpx.AsyncClient() as c:

                    for game_group in chunker(db_data, 10):
                        res = await c.request("POST", url="https://api.igdb.com/v4/games", content=f'''f name, genres.name, cover.image_id, first_release_date,platforms.id, platforms.abbreviation, url; where id = ({",".join([str(g["id"]) for g in game_group])});
                        ''', headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})

                        api_data += res.json()

                    api_data_mapped = {el['id']: el for el in api_data}

                    for db_entry in db_data:
                        id_key = db_entry['id']
                        try:
                            api_entry = api_data_mapped[id_key]
                        except:
                            continue
                        db_entry.update(api_entry)

            return json({"games": db_data})    


@app.get("/mygames")
async def get_games(request):
    try:
        userid = jwt.decode(request.cookies.get("token"),
                            JWT_SECRET, algorithms=['HS256'])["id"]

        db_data = []
        async with app.ctx.pool.acquire() as con:
            t = await con.fetchrow("SELECT review_template from Users where id = $1;", userid)
            template = t.get("review_template")
            rows = await con.fetch("SELECT id, rating, description, hours, played_platform from Games where username = $1;", userid)
            db_data = [{"id": int(row["id"]), "rating": str(row.get('rating')), "description": row.get(
                'description'), "hours": row.get('hours'), "played_platform": row.get('played_platform')} for row in rows]

        if len(db_data) > 0:
            api_data = []
            async with httpx.AsyncClient() as c:

                for game_group in chunker(db_data, 10):
                    res = await c.request("POST", url="https://api.igdb.com/v4/games", content=f'''f name, genres.name, cover.image_id, first_release_date,platforms.id, platforms.abbreviation, url; where id = ({",".join([str(g["id"]) for g in game_group])});
                    ''', headers={"Client-ID": IGDB_ID, "Authorization": f"Bearer {app.ctx.igdb_token}"})

                    api_data += res.json()

                api_data_mapped = {el['id']: el for el in api_data}

                for db_entry in db_data:
                    id_key = db_entry['id']
                    try:
                        api_entry = api_data_mapped[id_key]
                    except:
                        continue
                    db_entry.update(api_entry)

        return json({"template": template, "games": db_data})

    except jwt.exceptions.DecodeError:
        return json({"error": "Invalid token"}, status=401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
