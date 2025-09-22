from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church_donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    donations = db.relationship('Donation', backref='donor', lazy=True)

    def __repr__(self):
        return f'<Donor {self.first_name} {self.last_name}>'

class DonationType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    donations = db.relationship('Donation', backref='donation_type', lazy=True)

    def __repr__(self):
        return f'<DonationType {self.name}>'

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    donation_type_id = db.Column(db.Integer, db.ForeignKey('donation_type.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Donation ${self.amount} on {self.donation_date}>'

# Routes
@app.route('/')
def index():
    recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(5).all()
    total_donations = db.session.query(db.func.sum(Donation.amount)).scalar() or 0
    donor_count = Donor.query.count()
    return render_template('index.html', 
                         recent_donations=recent_donations,
                         total_donations=total_donations,
                         donor_count=donor_count)

@app.route('/donors')
def donors():
    page = request.args.get('page', 1, type=int)
    donors = Donor.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('donors.html', donors=donors)

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        donor = Donor(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'] if request.form['email'] else None,
            phone=request.form['phone'] if request.form['phone'] else None,
            address=request.form['address'] if request.form['address'] else None
        )
        try:
            db.session.add(donor)
            db.session.commit()
            flash('Donor added successfully!', 'success')
            return redirect(url_for('donors'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding donor. Email may already exist.', 'error')
    
    return render_template('add_donor.html')

@app.route('/donations')
def donations():
    page = request.args.get('page', 1, type=int)
    donations = Donation.query.order_by(Donation.donation_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('donations.html', donations=donations)

@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        donation = Donation(
            amount=float(request.form['amount']),
            donation_date=datetime.strptime(request.form['donation_date'], '%Y-%m-%d').date(),
            notes=request.form['notes'] if request.form['notes'] else None,
            donor_id=int(request.form['donor_id']),
            donation_type_id=int(request.form['donation_type_id'])
        )
        try:
            db.session.add(donation)
            db.session.commit()
            flash('Donation recorded successfully!', 'success')
            return redirect(url_for('donations'))
        except Exception as e:
            db.session.rollback()
            flash('Error recording donation.', 'error')
    
    donors = Donor.query.all()
    donation_types = DonationType.query.all()
    return render_template('add_donation.html', donors=donors, donation_types=donation_types)

@app.route('/reports')
def reports():
    # Monthly summary
    monthly_totals = db.session.query(
        db.extract('year', Donation.donation_date).label('year'),
        db.extract('month', Donation.donation_date).label('month'),
        db.func.sum(Donation.amount).label('total')
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # By donation type
    type_totals = db.session.query(
        DonationType.name,
        db.func.sum(Donation.amount).label('total')
    ).join(Donation).group_by(DonationType.name).all()
    
    return render_template('reports.html', 
                         monthly_totals=monthly_totals,
                         type_totals=type_totals)

def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Check if donation types already exist
    if DonationType.query.count() == 0:
        # Add default donation types
        donation_types = [
            DonationType(name='Tithe', description='Regular tithe contributions'),
            DonationType(name='Offering', description='General offerings'),
            DonationType(name='Special Donation', description='Special project donations'),
            DonationType(name='Building Fund', description='Contributions for building projects'),
            DonationType(name='Missions', description='Missionary support donations')
        ]
        
        for dt in donation_types:
            db.session.add(dt)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)