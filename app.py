from flask import Flask,render_template,request
import chatapp as a
from threading import Thread
app=Flask(__name__,template_folder="templates",static_folder="static",static_url_path="/static")

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result",methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    ch = a.ChatApplication()
    ch.run()
    return render_template("index.html")
if __name__=='__main__':
    #app.run(debug=True,port=5001)
    pass

