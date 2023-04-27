from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Create the database and user table if they don't exist
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id TEXT,
              name TEXT,
              email TEXT,
              password TEXT)''')
conn.commit()



# adding some dummy users
c.execute('''INSERT INTO users VALUES("1", "user1", "user1@example.com", "password")''')
c.execute('''INSERT INTO users VALUES("2", "user2", "user2@example.com", "password")''')
c.execute('''INSERT INTO users VALUES("3", "admin", "admin@example.com", "admin")''')
conn.commit()
conn.close()

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        c.execute("SELECT id, name FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid email or password.')
        conn.close()
    else:
        return render_template('login.html')


# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        if user:
            return render_template('signup.html', error='Email already exists.')
        else:
            c.execute("INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)", (id, name, email, password))
            conn.commit()
            conn.close()
            session['user_id'] = id
            session['user_name'] = name
            return redirect(url_for('profile'))
    else:
        return render_template('signup.html')

# User profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        if 'user_id' in session:
            user_id = session['user_id']
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT name, email FROM users WHERE id=?", (user_id,))
            user = c.fetchone()
            conn.close()
            if user:
                user_dict = {
                    'name': user[0],
                    'email': user[1]
                }
                return render_template('profile.html', user=user_dict)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        user_id = session['user_id']
        new_email = request.form['email']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT name, email FROM users WHERE id=?", (user_id,))
        c.execute("UPDATE users SET email=? WHERE id=?", (new_email, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('profile'))



# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
