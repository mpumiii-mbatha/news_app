# NewsApp Application
A Django application for managing and publishing news articles and newsletters.

## Description
NewsApp is a role-based publishing system that allows **journalists**, **editors**, **publishers**, and **readers** to interact with articles and newsletters.
Journalists can write content, editors can review and approve, publishers can publish final articles, and readers can subscribe and read publicly available posts.

## Table of Contents
- Introduction
- Installation
- MySQL/MariaDB Setup
- Usage
- Twitter API Instructions
- Running Tests
- Contributing
- License

## Introduction
NewsApp simulates a real-world newsroom workflow using Django.
It provides structured content creation, editing, approval, and publishing.
Readers can subscribe to newsletters, while staff members manage editorial content with permission-based access.

## Installation
1. Clone or download the zip file containing the NewsApp Django project.
2. Navigate to the project directory in your terminal.
3. Create and activate a virtual environment:

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
4. Install dependencies

## MariaDB Installation
1. Run the following command in your terminal:
    mysql -u root -p
2. Enter password:
    Mpumi777
3. Create the database by running the file:
    ./create_db.bat
4. Enter password:
    Mpumi777
5. Run migrations

## Twitter API Testing
1. Open cd news_app to access the directory in which the twitter_test.py is saved
2. Run **twitter_test.py** in the terminal under news_app(1)/news_app
4. Expected output:
    Initializing Twitter test…
   Sending test tweet...
   Tweet posted successfully: 1996487254190047530

   ----- RESULT -----
   {'text': '🌐 Twitter API Test — Sent from testing script', 'edit_history_tweet_ids': ['1996487254190047530'], 'id':         '1996487254190047530'}
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
