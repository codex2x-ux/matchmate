from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'matchmate-secret-2026'

# Login / Root
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Home
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Activities
@app.route('/activities')
def activities():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('activities.html', username=session['username'])

# Sports
@app.route('/sports')
def sports():
    if 'username' not in session:
        return redirect(url_for('login'))
    mode = request.args.get('mode', 'watch')
    return render_template('sports.html', username=session['username'], mode=mode)

# Profile
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)