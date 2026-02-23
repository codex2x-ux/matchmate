from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth as fb_auth

# Initialize Firebase Admin ONCE at startup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = 'matchmate-secret-2026'

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('profile'))
    return redirect(url_for('login'))


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# HOME
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])


# ACTIVITIES
@app.route('/activities')
def activities():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('activities.html', username=session['username'])


# PLAY TOGETHER
@app.route('/play')
def play():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('play_together.html', username=session['username'])



# GYM MATE
@app.route('/gym')
def gym():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('gymmate.html', username=session['username'])

# WATCH TOGETHER
@app.route('/watch')
def watch():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('watch_together.html', username=session['username'])


# GEAR SHARE
@app.route('/gear')
def gear():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('gearshare-rental.html', username=session['username'])


# PROFILE
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

# FIREBASE SESSION  ← ADD THIS
@app.route('/firebase-session', methods=['POST'])
def firebase_session():
    data         = request.get_json()
    id_token     = data.get('idToken', '')
    display_name = data.get('displayName', 'User')

    try:
        decoded = fb_auth.verify_id_token(id_token)
        session['username'] = decoded.get('name') or decoded.get('email') or display_name
        session['uid']      = decoded.get('uid')
        session['email']    = decoded.get('email')
        return jsonify({'status': 'ok'})
    except Exception as e:
        print("Firebase token error:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)