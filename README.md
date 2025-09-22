# Church Donation Contribution Tracker

A comprehensive web-based application for tracking and managing church donations and contributions. This Flask-based application provides an intuitive interface for recording donations, managing donors, and generating reports.

## Features

### Core Functionality
- **Donor Management**: Add, view, and manage donor information including contact details
- **Donation Recording**: Record donations with amount, date, type, and notes
- **Donation Types**: Support for various donation categories (Tithe, Offering, Special Donations, Building Fund, Missions)
- **Dashboard**: Overview of total donations, donor count, and recent activity
- **Reports**: Monthly summaries and donation type breakdowns

### User Interface
- Clean, responsive web interface using Bootstrap 5
- Mobile-friendly design
- Intuitive navigation and forms
- Real-time feedback with flash messages

## Technology Stack

- **Backend**: Python Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, Font Awesome icons
- **Styling**: Custom CSS with responsive design

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Final-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to `http://127.0.0.1:5000`

### First Time Setup

When you first run the application, it will automatically:
- Create the SQLite database (`church_donations.db`)
- Set up the database tables
- Add default donation types (Tithe, Offering, Special Donation, Building Fund, Missions)

## Usage Guide

### Adding Donors
1. Navigate to "Donors" in the main menu
2. Click "Add New Donor"
3. Fill in the donor information (First Name and Last Name are required)
4. Click "Add Donor"

### Recording Donations
1. Navigate to "Donations" in the main menu
2. Click "Record New Donation"
3. Select the donor from the dropdown
4. Choose the donation type
5. Enter the amount and date
6. Add optional notes
7. Click "Record Donation"

### Viewing Reports
1. Navigate to "Reports" in the main menu
2. View monthly totals and donation type summaries
3. Use the quick action buttons to navigate to other sections

## Database Schema

### Donor Table
- `id`: Primary key
- `first_name`: Donor's first name (required)
- `last_name`: Donor's last name (required)
- `email`: Email address (optional, unique)
- `phone`: Phone number (optional)
- `address`: Physical address (optional)
- `created_at`: Timestamp when donor was added

### Donation Table
- `id`: Primary key
- `amount`: Donation amount (required)
- `donation_date`: Date of donation (required)
- `notes`: Optional notes about the donation
- `donor_id`: Foreign key to Donor table
- `donation_type_id`: Foreign key to DonationType table
- `created_at`: Timestamp when donation was recorded

### DonationType Table
- `id`: Primary key
- `name`: Type name (required, unique)
- `description`: Description of the donation type

## File Structure

```
Final-Project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── donors.html      # Donor listing
│   ├── add_donor.html   # Add donor form
│   ├── donations.html   # Donation listing
│   ├── add_donation.html # Add donation form
│   └── reports.html     # Reports page
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
└── instance/            # Instance folder (ignored by git)
    └── church_donations.db # SQLite database
```

## Configuration

The application uses the following default configuration:
- **Secret Key**: Change the secret key in `app.py` for production use
- **Database**: SQLite database stored in `instance/church_donations.db`
- **Debug Mode**: Enabled by default (disable for production)

## Development

### Running in Development Mode
The application runs in debug mode by default, which enables:
- Automatic reloading when code changes
- Detailed error messages
- Interactive debugger

### Customization
- Modify donation types in the `init_db()` function
- Customize styling in `static/css/style.css`
- Add new routes and functionality in `app.py`

## Production Deployment

For production deployment:
1. Change the secret key in `app.py`
2. Disable debug mode
3. Use a production WSGI server like Gunicorn
4. Consider using PostgreSQL or MySQL for larger datasets
5. Implement proper backup procedures for the database

## Security Considerations

- The application includes basic form validation
- Email uniqueness is enforced at the database level
- Flash messages provide user feedback
- CSRF protection is provided by Flask's built-in features

## Contributing

This is a final project for Week 4. For improvements or bug fixes:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes as part of a Week 4 final project.

## Support

For questions or issues, please refer to the documentation above or contact the project maintainer.
