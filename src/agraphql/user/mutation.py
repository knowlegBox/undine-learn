from typing import Any
import re

from django.contrib.auth.hashers import make_password
from undine import MutationType, Input, GQLInfo

from api import models

def wright_email(email: str) -> str:
    # Utilisez re.match ou re.search
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.[\w]{2,4}$", email):
        raise ValueError("Email must be a valid email address")
    return email

def email_manager(email: str) -> str: # Renvoie le str, pas un bool
    if models.User.objects.filter(email=email).exists():
        raise ValueError("Email already exists")
    return wright_email(email) # Renvoie l'email validé


def email_manager(email: str) -> bool:
    if models.User.objects.filter(email=email).exists():
        raise ValueError("Email already exists")
    else:
        wright_email(email)
        return True
    
def username_manager(username: str) -> str:
    if models.User.objects.filter(username=username).exists():
        raise ValueError("Username already exists")
    else:
        return username

class UserMutation(MutationType[models.User], kind="create"):
    username = Input(str)
    first_name = Input(str)
    last_name = Input(str)
    email = Input(str)
    password = Input(str)
    bio = Input(str)
    profile_picture = Input(str)
    @classmethod
    def __mutate__(cls, instance: models.User, info: GQLInfo, input_data: dict[str, Any]) -> models.User:
        email = input_data.pop("email")
        password = input_data.pop("password")
        input_data["email"] = email_manager(email)
        input_data["password"] = make_password(password)
        input_data["username"] = username_manager(input_data["username"])
        user = models.User.objects.create(**input_data)
        return user


