from flask import Flask, render_template, request, redirect, url_for
from werkzeug.serving import run_simple

app = Flask(__name__)

# Sample in-memory data storage
users = []

@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists (for demonstration, using in-memory list)
        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect(url_for('dashboard'))
        
        return "Credenciais inválidas. Tente novamente."
    
    return render_template('login.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Save user data (here in memory, you can use a database instead)
        users.append({
            'name': name,
            'email': email,
            'username': username,
            'password': password
        })
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Dashboard after login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 0000, app)
