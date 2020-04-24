import os
from flask import Flask, session, request, render_template, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import User

app = Flask(__name__, template_folder="templates")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# # @app.route("/register", methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'post':
# #         username = request.form['username']
# #         password = request.form["password"]
# #         return(username+" "+password)
# #     else:
# #         return render_template('register.html')

# @app.route("/elegiblity", methods=["POST", "GET"])
# def elegiblity():
#     if request.method == 'GET':
#         return render_template("home.html")
#     name = request.form.get("username")
#     password = request.form.get("password")
#     return render_template("success.html", message = "Successfully Registered")

@app.route("/")
def index():
    valid_users = db.query(User).all()
    return render_template("home.html",users = valid_users)

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", message="please register")

@app.route("/elegiblity", methods=["POST", "GET"])
def elegiblity():
    if request.method == 'GET':
        return render_template("home.html")
    name = request.form.get("username")
    password = request.form.get("password")
    # if(db.query(User).filter_by(username=name)== None):
    details = User(username = name, password = password)
    details.set_password(password)
    db.add(details)
    db.commit()
    return render_template("success.html", message = "Successfully Registered")
    # else:
    #     return render_template("register.html", message= "please login, you have already registered")

@app.route("/sendtologin")
def sendtologin():
    return render_template("login.html")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("home.html")
    name = request.form.get("username")
    password = request.form.get("password")
    if(db.query(User).filter_by(username=name)!= None):
        details = db.query(User).get(name)
        if(password == details.password):
            return render_template("success.html", message = name)
        else:
            return render_template("login.html", message = "incorrect password")
    else:
        return render_template("register.html", message="you haven't registered please register first")

# def main():
    # db.create_all()
    # print("tables created")
    

# if __name__ == '__main__':
#     with app.app_context():
#         main()
    
