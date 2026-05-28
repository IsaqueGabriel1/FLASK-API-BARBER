from app import app
from app.view import home
from app.view import create
from app.view import delete
from app.view import update


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

