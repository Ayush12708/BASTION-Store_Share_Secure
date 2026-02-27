# BASTION - Secure File Storage

A Django-based secure file storage application with AWS S3 integration.

## Features

- User authentication (signup, login, logout)
- Secure file upload and download
- AWS S3 integration for file storage
- User dashboard with file management
- Audit logs for file operations
- Profile management

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: MySQL (AWS RDS)
- **Storage**: AWS S3
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ayush12708/BASTION-Store-Secure-Secure.git
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials in `finalproject/settings.py`:
```python
AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
AWS_S3_REGION_NAME = 'your_region'
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

```
finalproject/
├── accounts/              # Django app for user management
│   ├── migrations/        # Database migrations
│   ├── static/           # Static files (CSS, JS, images)
│   ├── templates/        # HTML templates
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── finalproject/         # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
└── requirements.txt
```

## Usage

- Access the application at `http://13.61.21.177`
- Register a new account or login
- Upload and manage your files securely

## License

MIT License

