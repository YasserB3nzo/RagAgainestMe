"""Shared practice data: a tiny repository, a toy embedding table and evaluation questions."""

REPO_NAME = "tiny-shop"
COMMIT = "a1b2c3d"

# A miniature code repository, like the ones your real assistant will index.
REPO = {
    "auth.py": '''import hashlib


def hash_password(password: str, salt: str) -> str:
    """Hash a password with a salt using SHA-256."""
    return hashlib.sha256((salt + password).encode()).hexdigest()


def login_user(username: str, password: str, users: dict) -> bool:
    """Check a username and password against the stored hashes."""
    record = users.get(username)
    if record is None:
        return False
    return hash_password(password, record["salt"]) == record["hash"]
''',
    "cart.py": '''def add_item(cart: dict, item: str, quantity: int = 1) -> None:
    """Add an item to the shopping cart."""
    cart[item] = cart.get(item, 0) + quantity


def remove_item(cart: dict, item: str) -> None:
    """Remove an item from the shopping cart."""
    cart.pop(item, None)


def total_price(cart: dict, prices: dict) -> float:
    """Compute the total price of the cart, including tax."""
    subtotal = sum(prices[item] * qty for item, qty in cart.items())
    return round(subtotal * 1.2, 2)
''',
    "README.md": '''# Tiny Shop

A small example shop used for RAG practice.

## Install

Create a virtual environment, then install the requirements with pip.

## Run with Docker

Build the image, then start the container with docker compose up.
The shop listens on port 8000.

## Security

Passwords are never stored in plain text. They are hashed with a salt.
''',
}

# A toy embedding model: each known word has a 4-number vector.
# The four dimensions are named only so you can read them:
#   [security, shopping, setup, general]
# Real models (like BGE-M3) learn 1024 unnamed dimensions instead.
WORD_VECTORS = {
    # security
    "password": [0.9, 0.0, 0.0, 0.1], "passwords": [0.9, 0.0, 0.0, 0.1],
    "hash": [0.8, 0.0, 0.0, 0.2], "hashed": [0.8, 0.0, 0.0, 0.2], "hashes": [0.8, 0.0, 0.0, 0.2],
    "salt": [0.7, 0.0, 0.0, 0.2], "login": [0.8, 0.1, 0.0, 0.1], "username": [0.6, 0.1, 0.0, 0.2],
    "user": [0.5, 0.2, 0.0, 0.3], "users": [0.5, 0.2, 0.0, 0.3], "security": [0.9, 0.0, 0.1, 0.0],
    "secure": [0.9, 0.0, 0.0, 0.1], "sha256": [0.8, 0.0, 0.0, 0.1], "stored": [0.4, 0.0, 0.1, 0.4],
    # shopping
    "cart": [0.0, 0.9, 0.0, 0.1], "item": [0.0, 0.8, 0.0, 0.2], "items": [0.0, 0.8, 0.0, 0.2],
    "price": [0.0, 0.9, 0.0, 0.1], "prices": [0.0, 0.9, 0.0, 0.1], "total": [0.0, 0.7, 0.0, 0.3],
    "tax": [0.0, 0.8, 0.0, 0.1], "shop": [0.1, 0.8, 0.1, 0.1], "shopping": [0.0, 0.9, 0.0, 0.1],
    "quantity": [0.0, 0.7, 0.0, 0.3], "subtotal": [0.0, 0.8, 0.0, 0.2], "cost": [0.0, 0.9, 0.0, 0.1],
    "buy": [0.0, 0.9, 0.0, 0.1], "remove": [0.0, 0.5, 0.0, 0.5], "add": [0.0, 0.5, 0.0, 0.5],
    # setup
    "install": [0.0, 0.0, 0.9, 0.1], "docker": [0.0, 0.0, 0.9, 0.1], "container": [0.0, 0.0, 0.8, 0.2],
    "image": [0.0, 0.0, 0.7, 0.2], "compose": [0.0, 0.0, 0.8, 0.1], "environment": [0.0, 0.0, 0.8, 0.2],
    "requirements": [0.0, 0.0, 0.8, 0.2], "pip": [0.0, 0.0, 0.9, 0.1], "port": [0.0, 0.0, 0.8, 0.2],
    "run": [0.1, 0.1, 0.6, 0.3], "start": [0.0, 0.1, 0.6, 0.3], "setup": [0.0, 0.0, 0.9, 0.1],
    "virtual": [0.0, 0.0, 0.7, 0.2], "deploy": [0.0, 0.0, 0.9, 0.1],
}

# Evaluation questions with the file that really answers each one.
QUESTIONS = [
    {"question": "Which function hashes the password with SHA-256?", "answer_path": "auth.py"},
    {"question": "How is the cart total price computed with tax?", "answer_path": "cart.py"},
    {"question": "How do I start the shop with Docker?", "answer_path": "README.md"},
]
