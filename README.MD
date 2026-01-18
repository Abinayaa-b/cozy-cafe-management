Cozy Cafe Management System
Project Documentation

1. Project Overview

        Project Name: Cozy Cafe Management System 

        Type: Web-based Cafe Management Application

        Purpose: A comprehensive system to manage cafe operations including menu management, order taking, and bill generation.

2. Tech Stack 

        Backend
                Framework: Flask (Python web framework)
                Language: Python 3.x
                Database: SQLite3
                Session Management: Flask Sessions

        Frontend

                HTML5: Structure and templates 
                CSS3: Styling with custom design system
            

        Design

                Color Scheme: Warm cafe-themed palette (beige, brown, cream)
                Font: Poppins (Google Fonts)
                Design Style: Modern, cozy, and minimalistic


3. System Architecture

    Database Schema
        Users Table
            sql- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
                - username (TEXT)
                - password (TEXT)
                - role (TEXT) - 'owner' or 'staff'
        Menu Table  
            sql- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
                - item_name    (TEXT)
                - price (INTEGER)
                - available (TEXT) - 'Yes' or 'No'
        Orders Table
            sql- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
                - table_no (TEXT)
                - item_name (TEXT)
                - quantity (INTEGER)
                - total (INTEGER)
                - created_at (TEXT) - timestamp


4. Project Structure
cozy-cafe-management/
│
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── images/
│       └── logo.png            # Cafe logo
│
├── templates/
│   ├── login.html              # Login page
│   ├── admin_dashboard.html    # Owner dashboard
│   ├── staff_dashboard.html    # Staff dashboard
│   ├── menu.html               # Menu display
│   ├── order.html              # Order taking form
│   ├── orders.html             # Orders list
│   └── bill.html               # Bill receipt
│
├── app.py                      # Main Flask application
├── add_menu.py                 # Database menu population script
└── database.db                 # SQLite database file