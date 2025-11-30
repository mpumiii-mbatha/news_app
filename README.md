\# News App



\## Setup with Python venv

1\. Clone the repo: `git clone <repo\_url>`

2\. Create virtual environment: `python -m venv .venv`

3\. Activate venv: `.\\.venv\\Scripts\\activate`

4\. Install requirements: `pip install -r requirements.txt`

5\. Apply migrations: `python manage.py migrate`

6\. Run server: `python manage.py runserver`



\## Setup with Docker

1\. Ensure Docker is installed and running.

2\. Build Docker image: `docker build -t news\_app .`

3\. Run container: `docker run -p 8000:8000 news\_app`

4\. Access app at `http://localhost:8000`



\*\*Note:\*\* Add your own secrets (e.g., `.env` file) before running.



