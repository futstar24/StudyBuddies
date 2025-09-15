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

CORS(app, supports_credentials=True, origins=["https://e14062411cbd.ngrok-free.app"]) #add real domain here

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
        print(session["user"])
        print("asgerdhtjfy")
        return {"info":"log in successful"}
    except Exception as e:
        return {"result":"fail","info":str(e)}

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")

@app.route("/getUserEmail",methods = ["GET"])
def getUserEmail():
    try:
        return {"email":db.collection("Users").document(session["user"]).get().to_dict()["email"]}
    except Exception as e:
        print(e)
        return {"info":str(e)}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080, use_reloader=True)