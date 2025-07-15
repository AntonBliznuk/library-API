# DRF-library-practice

Task says that I have to choose from six to eight tasks from Coding Mandatory, I have chosen the first seven tasks from Coding Mandatory.

🚀 Local Installation Guide

Make sure you have Python 3

⸻

1️⃣ Clone the project:
```bash
git clone https://github.com/yourusername/DRF-library-practice.git
cd DRF-library-practice
```

⸻

2️⃣ Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

⸻

3️⃣ Install required packages:
```bash
pip install -r requirements.txt
```

⸻

4️⃣ Set up environment variables:

•	Copy the example environment file:
```bash
cp env.sample .env
```

•	Open .env and fill in your secrets.

⸻

5️⃣ Create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

⸻

6️⃣ Create a superuser (optional but helpful):
```bash
python manage.py createsuperuser
```

⸻

7️⃣ Launch the server:
```bash
python manage.py runserver
```
Now you can open http://127.0.0.1:8000/api/doc/swagger/ and start exploring the project!
