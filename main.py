from flask import Flask, redirect , request , render_template, url_for
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import flash
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/videos/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}
app.secret_key = os.urandom(24)

# SQLite database initialization

'''# Check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']'''


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

db = SQLAlchemy(app)





@app.route('/')
def hello():
    
    return render_template('head.html')
  
    
@app.route('/home')
def home():
    return render_template('head.html', content='home.html')

@app.route('/history')
def history():
    return render_template('head.html', content='history.html')

@app.route('/search')
def search():
    return render_template('head.html', content='search.html')

@app.route('/youraccount')
def youraccount():
    return render_template('head.html', content='youraccount.html')

'''@app.route('/contact')
def contact():
    return render_template('head.html', content='contact.html')'''

@app.route('/edit_profile')
def edit_profile():
    return render_template('head.html', content='edit_profile.html')

@app.route('/your_video')
def your_video():
    return render_template('head.html', content='your_video.html')

@app.route('/liked_video')
def liked_video():
    return render_template('head.html', content='liked_video.html')

@app.route('/video_upload')
def video_upload():
    
    
    return render_template('head.html', content='video_upload.html')

@app.route('/saved_video')
def saved_video():
    return render_template('head.html', content='saved_video.html')


@app.route('/register')
def register():    
    # Data to populate the dropdown list
    dropdown_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    return render_template('register.html', options=dropdown_options)

@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgotpass_1.html')

@app.route('/forgotpass_2')
def forgotpass_2():
    return render_template('forgotpass_2.html')

@app.route('/forgotpass_3')
def forgotpass_3():
    return render_template('forgotpass_3.html')


    
'''@app.before_first_request
def populate_categories():
    if security_question.query.count() == 0:
        db.session.add_all([
            security_question(name="Category 1"),
            security_question(name="Category 2"),
            security_question(name="Category 3")
        ])
        db.session.commit()'''

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phoneno = request.form['phoneno']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = generate_password_hash(password)
        hashed_password_confirm = generate_password_hash(confirm_password)
        age = request.form['age']
        gender = request.form['gender']
        security_question = request.form['security_question']
        ans = request.form['ans']
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if username already exists
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('SELECT * FROM register_user WHERE email=?', (email,))
        existing_user = c.fetchone()

        if existing_user:
            
            return render_template('register.html', errors='Username already exists!')
            
        
        # Insert data into SQLite database
        conn = sqlite3.connect('user.db', timeout=50.0)
        c = conn.cursor()
        if hashed_password == hashed_password_confirm:
            c.execute('''
            INSERT INTO register_user (firstname, lastname, email, phoneno, password, age, gender, security_question, ans, date_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (firstname, lastname, email, phoneno, password, age, gender, security_question, ans, date_time))
            conn.commit()
            conn.close()
        else:
            return render_template('register.html', error='password not matched')

        flash("User registered successfully!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists and password is correct
        conn = sqlite3.connect('user.db', timeout=50.0)
        c = conn.cursor()
        c.execute('SELECT * FROM register_user WHERE email=? AND password=?', (email,password))
        user = c.fetchone()
        conn.close()

        if user:  # Compare hashed password
             # Store username in session
            return redirect(url_for('hello'))
        else:
            return render_template('login.html', error='Invalid username or password')
            

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Route to handle video upload
'''@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file and allowed_file(file.video_filename):
        filename = secure_filename(file.video_filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Save the video metadata in the database
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('INSERT INTO videos (video_name, video_filename) VALUES (?, ?)', 
                  (file.filename, filename))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return "Invalid file type", 400'''

  
if __name__ == '__main__':
    app.run(debug=True)
