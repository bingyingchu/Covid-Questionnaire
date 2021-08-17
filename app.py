from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Database009@localhost/flask"
db=SQLAlchemy(app)

# set up the table in the database
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    positive = db.Column(db.String)
    awaiting_result = db.Column(db.String)
    self_isolate = db.Column(db.String)
    symptoms = db.Column(db.String)
    travel_history = db.Column(db.String)
    email = db.Column(db.String(120))
    name = db.Column(db.String)

    
    def __init__(self, positive, awaiting_result, self_isolate, symptoms, travel_history, email, name):
        self.positive = positive
        self.awaiting_result = awaiting_result
        self.self_isolate= self_isolate
        self.symptoms = symptoms
        self.travel_history = travel_history
        self.email = email
        self.name = name

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method =='POST':
        positive = request.form['positive']
        awaiting_result = request.form['awaiting_result']
        self_isolate = request.form['self_isolate']
        symptoms = request.form['symptoms']
        travel_history = request.form['travel_history']
        email = request.form['email']
        name = request.form['name']
        data=Data(positive, awaiting_result, self_isolate, symptoms, travel_history, email, name)
        db.session.add(data)
        db.session.commit()
        send_email(email)
        return render_template("/success.html")
        
            
if __name__ == '__main__':
    app.debug=True
    app.run()


