from flask import Flask, request
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "capstone-project-389607:asia-southeast2:scan-animal",  # Cloud SQL Instance Connection Name
            "pymysql",
            user="pig",
            password="pig123",
            db="db_animal",
            ip_type=IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
        )
        return conn
    
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"creator": getconn}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'animal_scanner'
 
mysql = MySQL(app)

jenis = ['air', 'darat']

class HelloWorld(Resource):
    def get(self):
        hewan = ['ayam', 'bebek', 'kucing']
        return {'hewan': hewan[0]}

    def post(self):
        
        return {'jenis': jenis}
    
    def delete(self):
        global jenis
        jenis.remove('darat')
        return {'jenis': jenis}

class RegisterResource(Resource):
    def get(self):
        pass

    def post(self):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
 
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT * FROM register WHERE email=%s""", (email, ))
            user = cursor.fetchall()
            if not user:
                cursor.execute(''' INSERT INTO register VALUES(NULL, %s, %s, %s)''', (username, email, password))
                mysql.connection.commit()
            cursor.close()
        return {'username': username, 'email': email}
    
class LoginResource(Resource):
    def get(self):
        pass
    
    def post(self):
        email = request.form['email']
        password = request.form['password']
 
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT * FROM login WHERE email=%s""", (email, ))
            user = cursor.fetchall()
            if not user:
                cursor.execute(''' INSERT INTO login VALUES(NULL, %s, %s)''', (email, password))
                mysql.connection.commit()
            cursor.close()
        return {'email': email}


api.add_resource(HelloWorld, '/')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)