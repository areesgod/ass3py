from datetime import datetime, timedelta
from flask import Flask
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import jwt

app = Flask(__name__)
conn = psycopg2.connect(host="localhost", port = 5432, database="sql", user="postgres", password="lenovo2001")
cur = conn.cursor()

cur.execute("SELECT * FROM usertable")
query_results = cur.fetchall()


@app.route('/login')
def login():

    auth = request.authorization

    for i in range(cur.rowcount):
        if auth and auth.username == query_results[i][1]:
            if auth.password == query_results[i][2]:
                token = jwt.encode({'user':auth.username, 'exp':datetime.utcnow() + timedelta(minutes = 30)}, str(app.config['SECRET_KEY']))

                sql = "UPDATE usertable SET token = %s WHERE id = %s"
                val = (token, query_results[i][0])
                cur.execute(sql, val)
                conn.commit()

                return jsonify({'token': token})
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


@app.route('/protected')
def protected():
    cur.execute("SELECT * FROM usertable")
    query_results = cur.fetchall()

    token = request.args.get('token')

    for j in range(3):
        if token == query_results[j][3]:
            return "<h1>Hello, token which is provided is correct </h1>"
        else:
            continue
    return "<h1>Hello, Could not verify the token </h1>"

print(type(login))
if __name__ == '__main__':
    app.run(debug=True)