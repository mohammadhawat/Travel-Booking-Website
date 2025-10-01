Horizon Travels WDAD ✈️

Developed by: Mohammad Hawat
Student ID: 24056361
Coursework Module: Web Development and Databases (WDAD)
Academic Year: 2024/25

Project Overview

Horizon Travels is a full-stack web application that allows users to register, book air journeys, manage their bookings, and interact with an intuitive interface. The project also includes a powerful admin backend for managing flights, users, and generating business reports.

This system was developed using Flask (Python), MySQL, HTML/CSS, and VSCode on macOS.

Technologies Used
	•	Python 3 (Flask web framework)
	•	MySQL (local database)
	•	HTML5 + CSS3 (frontend templates and styling)
	•	Jinja2 (template engine)
	•	MySQL Workbench (for DB management)
	•	VSCode on macOS

Key Features Implemented
User Functionality
	•	Register, login/logout, session management
	•	View and book flights
	•	Booking confirmation page + email preview
	•	Profile management + password change
	•	View & cancel previous bookings
Admin Features
	•	Admin login/logout
	•	Add/update/delete journeys (CRUD)
	•	View all bookings
	•	Update user information (name/email)
	•	Admin password manager (admin + user reset)
	•	Reports:
	•	Total revenue
	•	Monthly revenue
	•	Sales per journey
	•	Top 5 routes & users
	•	Routes in loss (revenue < £200)
Technical
	•	Fully working local MySQL connection via db_config.py
	•	Database pre-filled with 20+ official flight records
	•	Filters by travel day and class on booking page
	•	Admin dashboard with live data

How to Run
	1.	Create a virtual environment:
    python3 -m venv venv
    source venv/bin/activate

    2. Install dependancies 
    pip install -r requirements.txt

    3. Start MySQL and ensure database ht_booking_db is active

    4. Run the App
    python app.py

    Open browser at 
    http://127.0.0.1:5000

