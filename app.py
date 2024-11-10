import os
import random
import psycopg2
import flask
from flask_login import login_user, logout_user,current_user, LoginManager,UserMixin
import songinfo
from flask_sqlalchemy import SQLAlchemy
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '5115secretekey'

db = SQLAlchemy(app)
savedartist = []

class User(db.Model,UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    artist = db.Column(db.String(120))
    artistid = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.username}"

db.create_all()
#setting up songifo.py to song 
song = songinfo

# lists that are passed to welcome.html to render users artist info
currentartist = []
imgurl = []
album = []
preview = []

saveartlist= []
anum = 0
savedartist = []
saveid =[]

login_manager = LoginManager()
login_manager.init_app(app)
loggedout = False
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@app.route("/")
def main():
    return flask.render_template("index.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if flask.request.method == "POST":
        username = flask.request.form["uid"]
        user = User.query.filter_by(username=username).first()
        if flask.request.form["submitbtn"] == "Login":
            savedartist.clear()
            saveid.clear()
            pwd = flask.request.form["pid"]
            if user:
                if pwd == user.password:
                    login_user(user)
                    return flask.redirect("setdata")
                else:
                    flask.flash("Wrong Username or Password")
                    return flask.redirect("/")
            else:
                flask.flash("Wrong Username or Password")
                return flask.redirect("/")
        if flask.request.form["submitbtn"] == "New User":
            return flask.redirect("Signup")
@app.route("/logout")
def logout():
    savedartist.clear()
    album.clear()
    imgurl.clear()
    preview.clear()
    logout_user()
    flask.session.clear()
    print("logout uer=",current_user)
    return flask.redirect("/")
@app.route("/setdata",methods=['GET','POST'])

def setdata():
    if current_user.is_authenticated ==True:
        users  = current_user
        userdata = User.query.filter_by(username=users.username).all()
        for user in userdata:
            savedartist.append(user.artist)
            saveid.append(user.artistid)
        artist = savedartist.copy()        
        copyartist = saveid.copy()
        word = ""
        if word in artist:
            for word in savedartist:  # iterating on a copy of the list since to remove empty fields
                if word in artist:
                    savedartist.remove(word)
        if word in copyartist:
            for word in saveid: 
                if word in copyartist:
                    saveid.remove(word)
        #if the users has saved artist in db randomly select the artist and  search them in the spotify api
        if len(savedartist)>0:    
            num = random.randint(0,(len(savedartist)-1))
            song.searcharitst(savedartist[num])
            currentartist.clear()
            currentartist.append(savedartist[num])
            return flask.redirect("welcome")        
        #i did most of the project using the spotify search api instead of the artist top track api
        if len(saveid)>0:
            num = random.randint(0,(len(saveid)-1))
            song.idsearch(saveid[num])
            return flask.redirect("welcome")
        else:
            currentartist.clear
            currentartist.append("")
            return flask.redirect("welcome")
    else:
        return flask.redirect("/")

@app.route("/welcome", methods=["GET", "POST"])
def the_welcome():
    #this route handels the post form welecom.html 
    # it has to submit one for adding based on artistid and one based on artist name. 
    if flask.request.method == "POST":
        if flask.request.form["submitbtn"] == "addnew":
            newartist = flask.request.form["artistid"]
            user = User.query.filter_by(username=current_user.username,artist=newartist).first()
            print("trooblshooting search",user)
            if user:
                flask.redirect("update")
            if newartist=="" or newartist in savedartist: 
                #if the user has not enter artist do noting if the artist exist in users data bas do noting
                savedartist
            else:
                user = User(username=current_user.username,password=current_user.password,artist=newartist)
                db.session.add(user)
                savedartist.append(newartist)
                db.session.commit()
                print("added new artist")
                album.clear()
                imgurl.clear()
                preview.clear()
            if len(savedartist)>0:           
                num = random.randint(0,(len(savedartist)-1))
                song.searcharitst(savedartist[num])
                currentartist.clear()
                currentartist.append(savedartist[num])
                
        if flask.request.form["submitbtn"] == "addid":
            artid = flask.request.form["aid"]
            #checks if the artist id is valid    
            song.idsearch(artid)
            datacheck = song.artistname.copy()
            if len(datacheck)>0:
                newartist = song.aidname[0]
                if newartist in savedartist:
                    #if artist exists do noting
                    savedartist 
                else:
                    user = User(username=current_user.username,password=current_user.password,artist=newartist,artistid =artid)
                    db.session.add(user)
                    db.session.commit()                            
                    savedartist.append(newartist)
                if len(savedartist)>0:           
                    num = random.randint(0,(len(savedartist)-1))
                    song.searcharitst(savedartist[num])
                    currentartist.clear()
                    currentartist.append(savedartist[num])
        return flask.redirect("update")
    return flask.redirect("update")

@app.route("/Signup", methods=["GET", "POST"])
def newuser():
    
    users = User.query.all()
    artist = []
    username = []
    artname = []
    newartist = flask.request.form.get('artistid')
    newuser = flask.request.form.get('uid')
    newpass = flask.request.form.get('pid')
    artistid = flask.request.form.get('aid')
    
    #checking to see if the enter artist id is valid 
    #if valid set the artistid as the user artist id 
    # if user left the artist name blanc find the name of the artsit using the artist id.
    song.idsearch(artistid)
    artname = song.aidname.copy()
    if len(song.artistname)>0:
        artid = artistid
    elif len(song.artistname)>0 and newartist=="":
        if len(artname)>0:
            newartist = artname[0]
        artid = artistid
    else:
        artid = "";
    for user in users:
        artist.append(user.artist)
        username.append(user.username)
    if flask.request.method == "POST":
        if flask.request.form["submitbtn"] == "create":
            if newuser in username:
                flask.flash("account already exists")
                return flask.redirect("Signup")
            if newpass=="" or newuser=="":
                flask.flash("Please Enter Username or Password")
                return flask.redirect("Signup")
            else:
                user = User(username=newuser,password=newpass,artist=newartist,artistid =artid)
                db.session.add(user)
                db.session.commit()
                artist.append(newartist)
                return flask.redirect("/")
        if flask.request.form["submitbtn"] == "back":
            return flask.redirect("/")
    return flask.render_template("newuser.html")    
@app.route("/update",methods=['GET','POST'])
def updateapp():
    if current_user.is_authenticated ==True:
        album = []
        if loggedout:
            return flask.redirect("/")
        print("saved artist ",savedartist)
        
        if len(savedartist)>0:
            imgurl= song.imgurl.copy()
            album = song.songname.copy()
            preview = song.musiclink.copy()
            print(preview)
        print(currentartist)
        if len(album)>1:
            num = random.randint(0,(len(album)-1))
            return flask.render_template("welcome.html",artist= currentartist[0],song=album[num],preview=preview[num],url=imgurl[num],fvartists=savedartist)
        else:
            mylist={"You have not saved a favorite artist","to save artist use the search bar and click add artist"}
            return flask.render_template("welcome.html",artist= "no artist saved in database",song="",preview="",url="",fvartists=mylist)
    else:
        return flask.redirect("/")
