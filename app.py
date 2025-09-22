from flask import Flask,render_template, request, redirect, flash
import pymongo
import datetime
import os
import random
from bson import ObjectId
client=pymongo.MongoClient(os.getenv("MONGO_URI"), tls=True, tlsAllowInvalidCertificates=True, )
db=client.jumbled_words
words=db.words

app=Flask(__name__)
app.secret_key=os.urandom(14)
@app.route("/",methods=["GET","POST"])
def home():
       if request.method=="GET":
              return render_template("home.html")
       else:
             word={}
             word["word"]=request.form["word"]
             words.insert_one(word)
             flash("Succesefully added word.")
             return redirect("/")

@app.route("/play", methods=["GET","POST"])
def play():
      if request.method=="GET":
            x=list(words.find({}))
            y=[]
            random.shuffle(x)
            for i in range(0,5,1):
                  l=list(x[i]["word"])
                  random.shuffle(l)
                  b="".join(l)
                  y.append({"word":b,"_id":x[i]["_id"]})
            print(y)
            return render_template("play.html", words=y)
      else:
            x=list(words.find({}))
            score=0
            correct_answers=[]
            user_answer=[]
            for i in x:
                  answer=request.form.get(str(i["_id"]))
                  if answer:
                        correct_answer=list(words.find({"_id":ObjectId(i["_id"])}))
                        correct_answers.append(correct_answer[0]["word"])
                        user_answer.append(answer)
                        if answer==correct_answer[0]["word"]:
                              score=score+1
            return render_template("score.html",ca=correct_answers, ua=user_answer, s=score)

if __name__=="__main__":
    app.run(debug=True)