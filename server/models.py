from dataclasses import dataclass
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
