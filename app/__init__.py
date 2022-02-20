from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for
import user

# here, you can import names of the local files

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/", methods=['GET', 'POST'])
def index():
  if 'username' not in session:  
    return render_template('login.html')
  
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satuday", "Sunday"]
  return render_template('dashboard.html', username=session['username'], days = days)

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
  method = request.method
  username = request.form.get('username')
  password = request.form.get('password')

  if method == 'GET':
    return redirect(url_for('index'))
  
  auth_state = user.auth_user(username, password)
  if auth_state == True:
      session['username'] = username
      return redirect(url_for('index'))
  elif auth_state == "bad_pass":
      return render_template('login.html', input="bad_pass")
  elif auth_state == "bad_user":
      return render_template('login.html', input="bad_user")

@app.route("/register", methods=['GET', 'POST'])
def register():
  return render_template('register.html')

@app.route("/rAuth", methods =['GET', 'POST'])
def rAuthenticate():
    ''' Authentication of username and passwords given in register page from user '''

    method = request.method
    username = request.form.get('username')
    password0 = request.form.get('password0')
    password1 = request.form.get('password1')

    if method == 'GET':
        return redirect(url_for('register'))

    if method == 'POST':
        if len(username) == 0:
            return render_template('register.html', given = "username")
        elif len(password0) == 0:
            return render_template('register.html', given = "password")
        else:
            if password0 != password1:
                return render_template('register.html', mismatch = True)
            else:
                user.create_db()
                if user.create_user(username, password0):
                    return render_template('login.html', input='success')
                else:
                    return render_template('register.html', taken = True)

@app.route("/create_activity", methods=['GET', 'POST'])
def create_activity():
  print("adsf")
  return render_template('create_activity.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  try:
    session.pop('username')
  except KeyError:
    return redirect(url_for('index'))
  return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run()