from dataclasses import dataclass
from sanic_motor import BaseModel
from datetime import datetime

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class SignupRequest:
    email: str
    username: str
    password: str   

@dataclass
class TokenReq:
    token: str

class User(BaseModel):
    __coll__ = "users"
    __unique_fields__ = ['username', 'email']

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.games= [{}]

#     # id = fields.IntField(pk=True)
#     # email = fields.CharField(256)
#     # username = fields.CharField(20)
#     # password = fields.CharField(64)
#     # created_at = fields.DatetimeField(auto_now_add=True)
#     # games = fields.ManyToManyField('models.Game', related_name='users')

#     class Meta:
#         table = "users"

#     def __str__(self):
#         return self.username

# class Game(Model):
#     igdb_id = fields.IntField(pk=True)

#     class Meta:
#         table = "games"
