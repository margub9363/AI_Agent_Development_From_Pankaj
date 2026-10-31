from datetime import datetime
import secrets
import string
import random

def get_current_time():
    """Returen the current date and time"""
    return datetime.now().strftime("%d-%m-%y %H:%M:%S")

def roll_dice():
    """Return a random number between 1 and 6"""
    return random.randint(1, 6)

def generate_password(length=12):
    """Generate a secure random password"""
    characters = (string.ascii_letters + string.digits + string.punctuation)
    password = ""
    for _ in range(length):
        password += secrets.choice(characters)
    return password
