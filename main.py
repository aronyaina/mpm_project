from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:useraro@db/main'
CORS(app)


@app.route('/')
def hello():
    return 'Hello , World !'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
