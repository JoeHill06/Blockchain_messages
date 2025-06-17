
from flask import *
import json

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def response():
    Username = "Joe"
    Password = "Joe"
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username",'')
        password = data.get("password",'')

        if username == Username and password == Password:
            print(f"Username: {username}, Password: {password}!")
            return json.dumps({"login":'success'})


if __name__ == "__main__":
    app.run(debug=True, port=5003)