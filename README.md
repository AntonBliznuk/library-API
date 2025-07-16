# DRF-library-practice

Task says that I have to choose from six to eight tasks from Coding Mandatory, I have chosen the first seven tasks from Coding Mandatory.

Here’s a clear, updated version of your installation guide for Docker Compose workflow:

⸻

🚀 Local Installation Guide

Make sure you have Docker and Docker Compose installed.

⸻

1️⃣ Clone the Project
```bash
git clone https://github.com/yourusername/DRF-library-practice.git
cd DRF-library-practice
```

⸻

2️⃣ Set Up Environment Variables
```bash
cp env.sample .env
```

Open .env and fill in your secrets.

⸻

3️⃣ Build and Run the Project with Docker Compose
```bash
docker-compose up --build
```
This will:

Install dependencies.

Create and apply migrations automatically.

Run the Django development server.

⸻

4️⃣ Access the Project

•	Open your browser and go to:
http://0.0.0.0:8000/api/doc/swagger/
