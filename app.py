from flask import Flask, render_template,request,redirect
import sqlite3
from speechaid import pronounce_word,listen_and_score
import random

word_to_analize=''
concat_str=""
def connect_db():
    conn = sqlite3.connect('Database.db', check_same_thread=False)
    return conn 
app = Flask(__name__)
@app.route("/") 
def index():
    return render_template("index.html") 
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM login_details WHERE email=? AND password=?",(email,password))
        result=cursor.fetchone()
        if result:
            return redirect("/home")
        else:
            return render_template("login.html",msg="Invalid Credentials !")
    return render_template("login.html")
@app.route("/sign_up",methods=['GET','POST'])
def sign_up():
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO login_details (username,email,password)VALUES(?,?,?)",(username,email,password))
        conn.commit()
        return render_template("sign_up.html",msg="Account Created Sucessfully !")
    return render_template("sign_up.html")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/main",methods=['GET','POST'])
def main():
    global concat_str
    words = ["Pa", "Ka", "Ma", "Sa", "Co", "Ga", "Gu"]
    concat_str=""
    for i in range(len(words)):
        concat_str=concat_str+words[i]+" ,"
    return render_template("words.html",words=concat_str)

@app.route("/test",methods=['GET','POST'])
def test():
    global concat_str
    words = ["Pa", "Ka", "Ma", "Sa", "Co", "Ga", "Gu"]
    concat_str=""
    for i in range(len(words)):
        concat_str=concat_str+words[i]+" ,"
    return render_template("test.html",words=concat_str)
@app.route("/test_pronounce",methods=['GET','POST'])
def test_pro():
   global word_to_analize,concat_str
   if request.method=="POST":
       words_with_spaces=request.form['words']
       word=words_with_spaces.replace(" ","")
       word_to_analize=word
       pronounce_word(word)
       return render_template("test.html",msg=word_to_analize,words=concat_str)

@app.route("/generate")
def gen():
    concat_str=""
    words = ["Pa", "Ka", "Ma", "Sa", "Co", "Ga", "Gu"]
    sequence_length=random.randint(1,5)
    sequence = random.choices(words, k=sequence_length)
    word = "".join(sequence)
    for i in range(0,7):
        concat_str=concat_str+words[i]+" ,"
    return render_template("words.html",words=concat_str,speek=word)

@app.route("/test_generate")
def test_gen():
    concat_str=""
    words = ["Pa", "Ka", "Ma", "Sa", "Co", "Ga", "Gu"]
    sequence_length=random.randint(1,5)
    sequence = random.choices(words,k=sequence_length)
    word = "".join(sequence)
    for i in range(0,7):
        concat_str=concat_str+words[i]+" ,"
    return render_template("test.html",words=concat_str,speek=word)
@app.route("/pronounce",methods=['GET','POST'])
def pro():
   global word_to_analize
   if request.method=="POST":
       words_with_spaces=request.form['words']
       word=words_with_spaces.replace(" ","")
       word_to_analize=word
       pronounce_word(word)
       return render_template("speek.html",msg=word_to_analize)
@app.route("/pro")
def pron():
    global word_to_analize
    pronounce_word(word_to_analize)
    return render_template("speek.html",msg=word_to_analize)

@app.route("/speek")
def speek():
    global word_to_analize
    spocken_word,score=listen_and_score(word_to_analize)
    return render_template("speek.html",spocken_word=spocken_word,score=score)
if __name__=="__main__":
    app.run(debug=True)