from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user, current_user
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))

# not all classes yet implemented
class Account(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # accountID = db.Column(db.Integer, nullable=False) # foreign key
    groupName = db.Column(db.String(80), nullable=False)
    groupDetails = db.Column(db.String(500), nullable=True)
    # groupLogFilePath = db.Column(db.String(500), nullable=False)
    playerList = db.Column(db.String(500), nullable=True)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# groupID = db.Column(db.Integer, nullable=False) # foreign id 1
	# currentCharacterID = db.Column(db.Integer, nullable=True) # playerID + characterID // foreign key 2
	noteContent = db.Column(db.String(500), nullable=True)

class GameMaster(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# accountID = db.Column(db.Integer, nullable=False) # foriegn key 1
	# groupID = db.Column(db.Integer, nullable=False) # foreign key 2
	noteContent = db.Column(db.String(500), nullable=True)

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# accountID = db.Column(db.Integer, nullable=False) # foreign key 1
 	# playerID = db.Column(db.Integer, nullable=False) # foreign key 2
	name = db.Column(db.String(80), nullable=False)
	bio = db.Column(db.String(500), nullable=True)
	image = db.Column(db.String(80), nullable=True) #file for saved img path probably
	# inventory = array or something?

class Stats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# characterID = db.Column(db.Integer, nullable=False) # foreign key
	statName = db.Column(db.String(80), nullable=False)
	diceAmount = db.Column(db.Integer, nullable=True)
	diceFaceValue = db.Column(db.Integer, nullable=True)
	statNumericValue = db.Column(db.Integer, nullable=True)

class UniqueField(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# characterID = db.Column(db.Integer, nullable=False) # foreign key
	fieldName = db.Column(db.String(80), nullable=False)
	details = db.Column(db.String(500), nullable=True)
	diceAmount = db.Column(db.Integer, nullable=True)
	diceFaceValue = db.Column(db.Integer, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password'] # may want to hash the password

		new_account = Account(username=username, email=email, password=password)
		db.session.add(new_account)
		db.session.commit()

		return redirect(url_for('login'))
	# else GET method:
	return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = Account.query.filter_by(username=username).first()

		if user and user.password == password:
            # login success
			login_user(user)
			return redirect(url_for('index')) # change from index to dashboard later
		else: # user/pass do not exist in db
			error = 'Invalid username or password'
			return render_template('login.html', error=error)

	return render_template('login.html')

@app.route('/database')
def database():
	accounts = Account.query.all()
	groups = Group.query.all()
	return render_template('database.html', accounts=accounts, groups=groups)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
	# needs code probably
	return render_template('dashboard.html') #need to pass needed variables

@app.route('/addgroup')
@login_required
def addgroup():
	return render_template('addgroup.html')

@app.route('/addcharacter')
@login_required
def addcharacter():
	return render_template('addcharacter.html')

if __name__ == '__main__':
	app.run(debug=True)