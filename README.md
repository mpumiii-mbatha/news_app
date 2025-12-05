# NewsApp Application
A Django application for managing and publishing news articles and newsletters.

## Description
NewsApp is a role-based publishing system that allows **journalists**, **editors**, **publishers**, and **readers** to interact with articles and newsletters.
Journalists can write content, editors can review and approve, publishers can publish final articles, and readers can subscribe and read publicly available posts.

## Documentation
Full project documentation, including API reference, can be found in newsapp/docs.

## This project includes:
- Role-based access control  
- Newsletter subscriptions  
- Twitter API integration  
- MariaDB/MySQL database  
- Docker deployment  
- REST API support

## Table of Contents
- Introduction  
- Requirements  
- Installation (Virtual Environment)  
- .env Example  
- MariaDB/Mysql Setup  
- Running the App (Virtual Environment)  
- Running the App in Docker  
- Twitter API Instructions  
- Running Tests  
- Documentation  
- Contributing  
- License 

## Introduction
NewsApp simulates a real-world newsroom workflow using Django.
It provides structured content creation, editing, approval, and publishing.
Readers can subscribe to newsletters, while staff members manage editorial content with permission-based access.

## Requirements
Before running the project, ensure you have the following installed:

- **Python 3.10+**
- **pip**
- **virtualenv** (optional)
- **Git**
- **MariaDB or MySQL**
- **Docker & Docker Compose**

## Installation
**Reviewers should download the zip file containing the NewsApp Django project.**
1. **Clone or extract the repository**
   ```bash
   git clone https://github.com/your-username/news_app.git
   cd news_app
2. Create and activate a virtual environment:

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies
   pip install -r requirements.txt
4. Create an .env file in the root directory:

   TWITTER_API_KEY=yourkey
   TWITTER_API_SECRET=yoursecret
   TWITTER_ACCESS_TOKEN=yourtoken
   TWITTER_ACCESS_SECRET=yoursecrettoken

## MariaDB Installation
1. Paste this exact code into your settings.py:

   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'newsapp_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
2. The code above ensures your mysql database is loaded on Docker
3. Uses the default host for Docker (db)
4. Run the following command in your terminal:
    mysql -u root -p
5. CREATE DATABASE newsapp_db or by running the file:
    ./create_db.bat
6. Ensure your settings and the create_db.bat match
   database credentials
7. Run Django migrations:
   python manage.py migrate
8. Create a superuser
   python manage.py createsuperuser

## Twitter API Testing
1. Ensure your .env file contains valid Twitter API credentials
2. Import your .env details into your settings.py by copying the code
   # Handling Twitter API
   env = environ.Env()
   environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

   # Twitter API Credentials
   TWITTER_CONSUMER_KEY = env('TWITTER_CONSUMER_KEY')
   TWITTER_CONSUMER_SECRET = env('TWITTER_CONSUMER_SECRET')
   TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN')
   TWITTER_ACCESS_TOKEN_SECRET = env('TWITTER_ACCESS_TOKEN_SECRET')
   TWITTER_BEARER_TOKEN = env('TWITTER_BEARER_TOKEN')
3. The twitter_api.py has the correct layout containing all the Twitter       keys (imported from settings) necessary for using your X developer         account
4. Navigate to the directory containing the script
5. Run **twitter_test.py** in the terminal under news_app(1)/news_app
6. Expected output:
    Initializing Twitter test…
   Sending test tweet...
   Tweet posted successfully: <tweet_id>

   ----- RESULT -----
   {'text': '🌐 Twitter API Test — Sent from testing script', ...'}
   ------------------

## Running the server in a Docker container
1. Make sure Docker is installed and running on your machine.

2. Build and start the containers:
    docker-compose up -d

3. This will contain the following:
    db running MariaDB 12.0
    web running the Django application
    The web container automatically waits
    for MariaDB to start before launching Django.

4. Apply Django migrations inside the web container:
    docker-compose exec web python
    news_app/ manage.py migrate

5. Run the server (if not already running with docker-compose up):
    docker-compose run web python
    news_app/manage.py runserver 0.0.0.0:8000

6. The app should now be accessible at
   http://localhost:8000/

## Documentation
Documentation is included in the /docs/ directory, containing:
1. Developer documentation
2. API documentation
3. Architecture notes

## Contributing

N/A

## License

MIT License

Copyright (c) 2025 mpumiii-mbatha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
