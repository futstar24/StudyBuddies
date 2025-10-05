from flask import *
from flask_cors import *
import pyrebase
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

firebaseConfig = {
    "apiKey": "AIzaSyDBA8i_AQDQBG3Ob3Lkj09cmogSn8FFrnY",
    "authDomain": "studybuddies-f9fbf.firebaseapp.com",
    "projectId": "studybuddies-f9fbf",
    "storageBucket": "studybuddies-f9fbf.firebasestorage.app",
    "messagingSenderId": "282425683880",
    "appId": "1:282425683880:web:b4663189da318746ae379d",
    "measurementId": "G-RLNMWPHKSB",
    "databaseURL":"",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

cred = credentials.Certificate("studybuddies-f9fbf-firebase-adminsdk-fbsvc-514adc0d82.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = "secret"

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

CORS(app, supports_credentials=True, origins=["https://85df9f4b0999.ngrok-free.app"]) #add real domain here

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
    
@app.route("/signUp/<email>/<password>",methods = ["GET"])
def signUp(email,password):
    try:
        user = auth.create_user_with_email_and_password(email,password)
        session["user"] = user["localId"]
        db.collection("Users").document(user["localId"]).set({"email":email})
        return {"message":email}
    except Exception as e:
        print(e)
        if "EMAIL_EXISTS" in str(e):
            return {"result":"login"}
        return {"result":"fail","info":str(e)}
    
@app.route("/logIn/<email>/<password>")
def logIn(email,password):
    try:
        user = auth.sign_in_with_email_and_password(email,password)
        session["user"] = user["localId"]
        return {"info":"log in successful"}
    except Exception as e:
        return {"result":"fail","info":str(e)}

@app.route("/logout")
def logout():
    try:
        session.pop("user")
        return {"result":"success"}
    except:   
        return {"result":"fail"}

@app.route("/getUserInformation",methods = ["GET"])
def getUserInformation():
    try:
        return {"result":"success","info":db.collection("Users").document(session["user"]).get().to_dict()}
    except Exception as e:
        print(e)
        return {"result":str(e)}
    
@app.route("/example")
def showExamplePage():
    return render_template("example.html", loggedIn = 1 if "user" in session.keys() else 0)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080, use_reloader=True)