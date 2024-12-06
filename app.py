import os
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from datetime import datetime


# Initialize the Flask app
app = Flask(__name__)

# Configuration settings
app.config['UPLOAD_FOLDER'] = 'uploads/cvs'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AutoJobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Secret key for sessions
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect here if user is not logged in

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Define the upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure that the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Client class
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='clients')

# Invoice class
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='invoices')

# User class with username
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    clients = db.relationship('Client', back_populates='user', lazy=True)
    invoices = db.relationship('Invoice', back_populates='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

# Activity class
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    status = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cv = db.Column(db.String(255), nullable=False)  # Store the file path (string)
    job_title = db.Column(db.String(255), nullable=False)
    job_location = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Applied")  # Track the status, like "Applied"
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<JobApplication {self.job_title} at {self.job_location}>'

# Define the ContactForm model
class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ContactForm {self.name}>'

class Dice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    jobTitle = db.Column(db.String(100), nullable=False)
    diceEmail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    dice_status = db.Column(db.String(50), default="stopped")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Ensure nullable=False

    user = db.relationship('User', backref='dice')

    def __repr__(self):
        return f'<Dice {self.fullName}>'

# Define the Payment model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    card_name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(19), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', backref='payments')

    def __repr__(self):
        return f"<Payment {self.id} - Plan: {self.plan}, User ID: {self.id}>"



# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in.', 'error')
            return redirect(url_for('login'))

        # Create new user with hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect(url_for('login'))
        else:
            flash('No account found with this email. Please sign up first.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        # Handle CV upload and form submission
        cv = request.files['cv']
        job_title = request.form['job-title']
        job_location = request.form['job-location']
        job_description = request.form['job-description']

        # Save the uploaded CV file with a secure name
        if cv and allowed_file(cv.filename):  # Check if the file is allowed
            filename = secure_filename(cv.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cv.save(file_path)  # Save the file to the server

            # Create a new job application entry
            job_application = JobApplication(
                cv=file_path,
                job_title=job_title,
                job_location=job_location,
                job_description=job_description,
                user_id=current_user.id,  # Set the user_id
                date_applied=datetime.utcnow()
            )
            db.session.add(job_application)
            db.session.commit()

            # After form submission, redirect to the GET route to prevent resubmission on page refresh
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid file format. Please upload a valid CV.", "error")

    # Fetch the applied jobs for the current user
    applied_jobs = JobApplication.query.filter_by(user_id=current_user.id).all()

    # Render the dashboard template with the applied jobs
    return render_template('dashboard.html', applied_jobs=applied_jobs)

@app.route('/dashboard/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    # Fetch the job application by ID and ensure it belongs to the logged-in user
    job = JobApplication.query.get(job_id)
    
    if job is None:
        flash('Job not found.', 'error')
        return redirect(url_for('dashboard'))

    if job.user_id != current_user.id:
        flash('You are not authorized to delete this job.', 'error')
        return redirect(url_for('dashboard'))

    # Delete the job application
    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/job/<int:job_id>', methods=['GET'])
def job_details(job_id):
    # Query the database for the specific job application by its ID
    job = JobApplication.query.get_or_404(job_id)
    
    # Render the job details template with the job data
    return render_template('job_details.html', job=job)

# Features, About, Contact, Pricing, and Payment routes
@app.route('/features')
def features():
    return render_template('features.html')


# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for displaying the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create a new contact form entry
        new_contact = ContactForm(name=name, email=email, message=message)

        # Add the new contact form entry to the database
        db.session.add(new_contact)
        db.session.commit()

        # Redirect to a thank you page (you can create this page later)
        return redirect(url_for('contact'))

    return render_template('contact.html')


# Route for pricing page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')



@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        # Get data from the form
        plan = request.form['plan']
        price = request.form['price']
        card_name = request.form['card-name']
        card_number = request.form['card-number']
        expiry_date = request.form['expiry-date']
        cvv = request.form['cvv']

        # Create a new Payment instance with the current user's ID
        new_payment = Payment(
        plan=plan,
        price=float(price),  # Ensure price is converted to float
        card_name=card_name,
        card_number=card_number,
        expiry_date=expiry_date,
        cvv=cvv,
        user_id=current_user.id  # Store the current user's ID
    )


        # Add and commit the payment to the database
        db.session.add(new_payment)
        db.session.commit()

        return redirect(url_for('payment'))

    # Render the payment form
    plan = request.args.get('plan')
    price = request.args.get('price')
    return render_template('payment.html', plan=plan, price=price)


@app.route('/bots')
def bots():
    return render_template('bots.html')

@app.route('/diceDashboard', methods=['GET', 'POST'])
@login_required
def diceDashboard():
    dice_entries = Dice.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        # Collect form data
        fullName = request.form.get('fullName')
        jobTitle = request.form.get('jobTitle')
        diceEmail = request.form.get('diceEmail')
        password = request.form.get('password')

        # Add a new dice entry to the database with the current user's ID
        new_dice = Dice(
            fullName=fullName,
            jobTitle=jobTitle,
            diceEmail=diceEmail,
            password=password,
            user_id=current_user.id  # Set the foreign key to the logged-in user's ID
        )
        db.session.add(new_dice)
        db.session.commit()

        return redirect(url_for('diceDashboard'))

    return render_template('diceDashboard.html', dice_entries=dice_entries)


@app.route('/edit_dice/<int:dice_id>', methods=['GET', 'POST'])
@login_required
def edit_dice(dice_id):
    # Fetch the dice entry by ID
    dice = Dice.query.get_or_404(dice_id)

    # Ensure that the dice entry belongs to the logged-in user
    if dice.user_id != current_user.id:
        flash('You are not authorized to edit this entry.', 'error')
        return redirect(url_for('diceDashboard'))

    if request.method == 'POST':
        # Get updated data from the form
        dice.fullName = request.form.get('fullName')
        dice.jobTitle = request.form.get('jobTitle')
        dice.diceEmail = request.form.get('diceEmail')
        dice.password = request.form.get('password')

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('diceDashboard'))

    # Render the edit form with existing dice data
    return render_template('editDice.html', dice=dice)



@app.route('/delete_dice/<int:dice_id>', methods=['GET', 'POST'])
def delete_dice(dice_id):
    dice = Dice.query.get_or_404(dice_id)
    db.session.delete(dice)
    db.session.commit()
    return redirect(url_for('diceDashboard'))

@app.route('/toggle_dice_status', methods=['POST'])
def toggle_dice_status():
    # Get the action from the request
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action not in ['start', 'stop']:
            return jsonify({'success': False, 'message': 'Invalid action'})
        
        # Assuming you want to toggle a specific dice, get the dice instance
        dice = Dice.query.first()  # For example, get the first dice from the database
        
        if not dice:
            return jsonify({'success': False, 'message': 'Dice not found'})

        # Update dice status based on action
        if action == 'start':
            dice.dice_status = 'running'  # Set the dice to 'running'
        elif action == 'stop':
            dice.dice_status = 'stopped'  # Set the dice to 'stopped'
        
        # Commit the changes to the database
        db.session.commit()

        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Initialize the database and create tables if they don't exist
with app.app_context():
    db.drop_all()  # Be cautious with this in production environments
    db.create_all()  # Recreate all tables


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
