from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from forms import RegisterForm, LoginForm , CalculatorForm, DateRangeForm
from flask import render_template, request
from models import db , User , Maintenance , UsageData
from geopy.geocoders import Nominatim
import requests , datetime , os ,threading
import math
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5228'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')


# Utility functions
def get_sunlight_hours(lat, lon):
    api_key = "your_nrel_api_key"  # Replace with your NREL API Key
    url = f"https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['outputs']['avg_dni']['annual'] / 1000  # Convert Wh/m2 to kWh/m2
    return 5.5  # Default average sunlight hours


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = CalculatorForm()
    if form.validate_on_submit():
        energy_output = form.panel_capacity.data * form.sunlight_hours.data /1000
        installation_cost = form.number_of_panels.data * form.cost_per_panel.data
        annual_savings = energy_output * form.electricity_cost.data*365
        payback_period = installation_cost /annual_savings
        return render_template('results.html', energy_output=energy_output, installation_cost=installation_cost, \
                               annual_savings=annual_savings, payback_period=payback_period)
        
    return render_template('dashboard.html', form=form)

@app.route('/get_location', methods=['POST'])
def get_location():
    geolocator = Nominatim(user_agent="solar_app")
    location = geolocator.geocode(request.form['address'])
    if location:
        sunlight_hours = get_sunlight_hours(location.latitude, location.longitude)
        return {'latitude': location.latitude, 'longitude': location.longitude, 'sunlight_hours': sunlight_hours}
    return {'error': 'Unable to fetch location.'}

def send_message(to, message):
    print(f"Sending message to {to}: {message}")  # Replace with actual email/SMS integration

# ROI calculation thread
def calculate_roi_periodically():
    with app.app_context():
        while True:
            users = User.query.all()
            for user in users:
                usage_data = UsageData.query.filter_by(user_id=user.id).all()
                total_energy_used = sum([data.energy_used for data in usage_data])
                roi_message = f"Your total energy used so far: {total_energy_used} kWh. Keep saving!"
                send_message(user.email, roi_message)
            threading.Event().wait(30 * 24 * 60 * 60)  # Wait 30 days

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email, password=password).first()
        if user :
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html',form=form)


@app.route('/maintenance')
def maintenance():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access maintenance records.', 'warning')
        return redirect(url_for('login'))

    maintenance_records = Maintenance.query.filter_by(user_id=user_id).all()

    # Send reminder messages
    for record in maintenance_records:
        if not record.message_sent and record.maintenance_date <= datetime.date.today():
            user = User.query.get(user_id)
            send_message(user.email, f"Reminder: Maintenance scheduled on {record.maintenance_date}")
            record.message_sent = True
            db.session.commit()

    return render_template('maintenance.html', records=maintenance_records)

def calculate_subsidy(capacity, cost):

    if capacity <= 3:
        subsidy_percentage = 40  
    elif 3 < capacity <= 10:
        subsidy_percentage = 20
    else: 
        subsidy_percentage = 0 
    subsidy_amount = (subsidy_percentage / 100) * cost
    reduced_cost = cost - subsidy_amount
    return subsidy_percentage, subsidy_amount, reduced_cost


@app.route('/subsidies', methods=['GET', 'POST'])
def subsidies():
    if request.method == 'POST':
        try:
            # Get user inputs from the form
            capacity = float(request.form['capacity'])
            cost = float(request.form['cost'])
            
            # Calculate subsidy based on inputs
            subsidy_percentage, subsidy_amount, reduced_cost = calculate_subsidy(capacity, cost)
            
            # Render result in subsidies.html
            return render_template('subsidies.html', 
                                   subsidy_percentage=subsidy_percentage,
                                   subsidy_amount=subsidy_amount,
                                   reduced_cost=reduced_cost)
        except ValueError:
            return "Invalid input. Please ensure all fields are filled correctly."

    return render_template('sub_froms.html')


def calculate_subsidy(capacity, cost):
    # Define subsidy percentages based on capacity
    if capacity <= 3:
        subsidy_percentage = 40  # 40% subsidy for <= 3 kW
    elif 3 < capacity <= 10:
        subsidy_percentage = 20  # 20% subsidy for 3-10 kW
    else:
        subsidy_percentage = 0  # No subsidy for > 10 kW
    
    # Calculate subsidy amount and reduced cost
    subsidy_amount = (subsidy_percentage / 100) * cost
    reduced_cost = cost - subsidy_amount
    
    return subsidy_percentage, subsidy_amount, reduced_cost

def calculate_emi(principal, annual_interest_rate, tenure_years):
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    tenure_months = tenure_years * 12
    emi = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure_months) / \
          ((1 + monthly_interest_rate) ** tenure_months - 1)
    return emi

@app.route('/emi_options', methods=['GET', 'POST'])
def emi_options():
    if request.method == 'POST':
        try:
            # Get user inputs from the form
            total_cost = float(request.form['total_cost'])
            subsidy = float(request.form['subsidy'])
            down_payment = float(request.form['down_payment'])
            annual_interest_rate = float(request.form['annual_interest_rate'])
            tenure_years = int(request.form['tenure_years'])

            # Calculate loan amount and EMI
            loan_amount = total_cost - subsidy - down_payment
            emi = calculate_emi(loan_amount, annual_interest_rate, tenure_years)

            # Pass data to the template
            return render_template('emi_options.html',
                                   loan_amount=loan_amount,
                                   emi=emi,
                                   tenure_years=tenure_years)
        except ValueError:
            return "Invalid input. Please ensure all fields are filled correctly."
    # Render form for GET requests
    return render_template('emi_form.html')

@app.route('/roi_updates')
def roi_updates():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view ROI updates.', 'warning')
        return redirect(url_for('login'))
    usage_data = UsageData.query.filter_by(user_id=user_id).all()
    total_energy_used = sum([data.energy_used for data in usage_data])
    return render_template('roi_updates.html', total_energy_used=total_energy_used)

def orientation():
    return render_template('orientation.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)    
    session.pop('user_type', None)  
    flash('Logged out successfully!')
    return redirect(url_for('login'))   



if __name__ == '__main__':
    if not os.path.exists('solar.db'):
        with app.app_context():
            db.create_all()
    threading.Thread(target=calculate_roi_periodically, daemon=True).start()
    app.run(debug=True)
