# DevSearch

DevSearch is a platform designed for developers to showcase their projects, connect with other developers, share feedback, and collaborate. Built with Django and PostgreSQL, it provides a comprehensive ecosystem for developer networking and project discovery.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [Docker Setup](#docker-setup)
- [Testing](#testing)
- [Internationalization](#internationalization)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Features
* **Project Showcase** - Share and display your development projects with the community
* **Developer Profiles** - Create detailed profiles showcasing your skills and experience
* **Project Rating & Reviews** - Rate and provide feedback on other developers' projects
* **Real-time Messaging** - Message other developers directly through the platform
* **Search Functionality** - Advanced search to find developers and projects using PostgreSQL full-text search
* **Tag System** - Organize and discover projects using tags
* **User Authentication** - Secure session-based authentication with email verification
* **Multilingual Support** - Available in English and French

### Additional Features
* **Admin Dashboard** - Comprehensive admin interface powered by Django Jazzmin
* **Responsive Design** - Mobile-friendly UI
* **Image Management** - Cloudinary integration for image storage and optimization
* **Background Tasks** - Celery integration for asynchronous task processing
* **Caching** - Redis caching for improved performance
* **Static File Optimization** - WhiteNoise for efficient static file serving

## Tech Stack

### Backend
* **Django 5.1** - Python web framework
* **PostgreSQL** - Database with full-text search capabilities
* **Redis** - Caching and message broker
* **Celery** - Asynchronous task queue

### Frontend
* **HTML/CSS/JavaScript** - Frontend technologies
* **Bootstrap 5** - CSS framework
* **Crispy Forms** - Django form rendering
* **SweetAlert2** - Beautiful alert/notification system

### DevOps & Deployment
* **Docker & Docker Compose** - Containerization
* **WhiteNoise** - Static file serving
* **Cloudinary** - Media file storage
* **Gunicorn** - WSGI HTTP Server

### Development Tools
* **Django Debug Toolbar** - Development debugging
* **Rosetta** - Translation management
* **Django Extensions** - Additional Django utilities

## Project Structure

```
devsearch/
│
├── apps/                           # Django applications
│   ├── accounts/                   # User authentication & management
│   │   ├── management/commands/
│   │   │   └── populate_db.py      # Database seeding command
│   │   ├── migrations/
│   │   ├── templates/accounts/
│   │   │   ├── emails/             # Email templates
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── tests/
│   │   │   ├── test_forms.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── tasks.py                # Celery tasks
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── common/                     # Shared utilities & templates
│   │   ├── templates/common/
│   │   │   ├── base.html           # Base template
│   │   │   ├── index.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── templatetags/
│   │   │   └── custom_tags.py
│   │   ├── models.py               # BaseModel abstract class
│   │   ├── utils.py
│   │   └── views.py
│   │
│   ├── messaging/                  # Internal messaging system
│   │   ├── migrations/
│   │   ├── templates/messaging/
│   │   │   ├── inbox.html
│   │   │   ├── message_detail.html
│   │   │   └── message_form.html
│   │   ├── tests.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── profiles/                   # Developer profiles & skills
│   │   ├── migrations/
│   │   ├── templates/profiles/
│   │   │   ├── account.html        # User dashboard
│   │   │   ├── profile.html
│   │   │   ├── profiles_list.html
│   │   │   └── edit.html
│   │   ├── tests.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   │
│   └── projects/                   # Project showcase & reviews
│       ├── migrations/
│       ├── templates/projects/
│       │   ├── project_detail.html
│       │   ├── project_form.html
│       │   └── projects_list.html
│       ├── tests.py
│       ├── admin.py
│       ├── forms.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       ├── utils.py                # Search & pagination utilities
│       └── views.py
│
├── data/                           # Docker volumes (not in git)
│   ├── cache/                      # Redis data
│   └── db/                         # PostgreSQL data
│
├── deployment/                     # Deployment scripts
│   ├── celery                      # Celery startup script
│   └── docker-run                  # Docker entrypoint script
│
├── dev/                            # Django project configuration
│   ├── settings/
│   │   ├── base.py                 # Base settings
│   │   ├── dev.py          # Development settings
│   │   └── prod.py           # Production settings
│   ├── asgi.py
│   ├── celery.py                   # Celery configuration
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py
│
├── fixtures/                       # Sample data
│   └── devsearch.json
│
├── locale/                         # Internationalization
│   ├── en/LC_MESSAGES/
│   │   ├── django.po               # English translations
│   │   └── django.mo
│   └── fr/LC_MESSAGES/
│       ├── django.po               # French translations
│       └── django.mo
│
├── static/                         # Static files (source)
│   ├── images/                     # Project screenshots
│   ├── js/
│   │   └── main.js
│   ├── media/                      # Default images
│   ├── styles/
│   │   └── app.css
│   └── uikit/                      # UIKit library
│
├── staticfiles/                    # Collected static files (generated)
│
├── .dockerignore
├── .env                            # Environment variables (not in git)
├── .env.example                    # Environment template
├── .gitignore
├── build_files.sh                  # Build script
├── commands.txt                    # Useful commands
├── docker-compose.yml              # Production Docker config
├── docker-compose.dev.yml          # Development Docker config
├── Dockerfile
├── Dockerfile.dev
├── entrypoint.dev
├── manage.py                       # Django management script
├── Makefile                        # Development shortcuts
├── README.md
├── requirements.txt                # Python dependencies
└── wait-for-it.sh                  # Service readiness script
```

### Key Directories Explained

#### `/apps`
Contains all Django applications organized by functionality. Each app follows Django's standard structure with models, views, forms, templates, migrations, and tests.

#### `/apps/accounts`
Handles user authentication, registration, email verification, and user management. Includes Celery tasks for async email operations and custom managers for user models.

#### `/apps/common`
Shared utilities, base models (BaseModel abstract class), custom template tags, and common templates (base.html, pagination, error pages) used across the application.

#### `/apps/messaging`
Implements the internal messaging system allowing developers to communicate with each other through the platform.

#### `/apps/profiles`
Manages developer profiles, skills showcase, social links, and profile-related functionality including profile editing and skill management.

#### `/apps/projects`
Core functionality for project showcase, reviews, ratings, tags, and project management. Includes search and pagination utilities.

#### `/data`
Data persistence directory for Docker volumes containing PostgreSQL database files and Redis cache dumps. This directory is not tracked in version control.

#### `/dev`
Django project configuration with environment-specific settings (development, production), ASGI/WSGI configurations, main URL routing, and Celery setup.

#### `/fixtures`
JSON fixtures for seeding the database with sample data for development and testing purposes.

#### `/locale`
Translation files for internationalization (i18n) supporting multiple languages. Contains .po (portable object) files for translators and .mo (machine object) compiled files.

#### `/static`
Source static files (CSS, JavaScript, images, UIKit library) before collection. This is where you edit static assets during development.

#### `/staticfiles`
Collected and optimized static files for production (generated by `collectstatic` command). Includes Django admin, third-party packages, and custom static files.

## Prerequisites

* Python 3.12+
* PostgreSQL 14+
* Redis 6+
* Docker & Docker Compose (optional, for containerized setup)
* Git

## Installation

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/praise002/devsearch.git
cd devsearch
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
SETTINGS=development

# Database
POSTGRES_DB=devsearch_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Cloudinary (for media files)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0

# Flower (Celery monitoring)
FLOWER_PASSWORD=your-flower-password
```

5. **Set up PostgreSQL database**
```bash
# Create database using psql
# ON Windows OS
psql -U postgres
# On LInux
sudo -u postgres psql

CREATE USER username WITH PASSWORD 'XXXXX';
CREATE DATABASE devsearch_db OWNER general ENCODING 'UTF8';
CREATE EXTENSION pg_trgm;  # For full-text search
\q
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Load sample data (optional)**
```bash
python manage.py loaddata fixtures/devsearch.json
# Or populate with fake data
python manage.py populate_db
```

9. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

## Running the Application

### Local Development

1. **Start Redis** (in a separate terminal)
```bash
redis-server
```

2. **Start Celery worker** (in a separate terminal)
```bash
celery -A dev worker -l info --pool=solo
```

3. **Start Celery beat** (in a separate terminal)
```bash
celery -A dev beat -l info
```

4. **Run development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Using Makefile Commands

The project includes a Makefile with shortcuts:

```bash
# Database operations
make mmig              # Make migrations
make mig               # Run migrations
make dbshell           # Open database shell

# Server operations
make serv              # Run development server
make suser             # Create superuser

# Testing
make tests             # Run tests
make check             # Check for issues
make check-deploy      # Check deployment readiness

# Code quality
make lint              # Run linting and formatting

# Utilities
make help              # Show available commands
make secret-key        # Generate new secret key
```

## Docker Setup

### Development with Docker

1. **Build and start services**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. **Create superuser**
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

3. **Access services**
   - Web application: `http://localhost:8000`
   - Flower (Celery monitoring): `http://localhost:5555`
   - Admin: `http://localhost:8000/admin`


### Docker Services

The Docker Compose setup includes:
- **web** - Django application (Gunicorn)
- **db** - PostgreSQL database
- **redis** - Redis cache and message broker
- **celery-worker** - Celery worker for background tasks
- **celery-beat** - Celery beat for scheduled tasks
- **flower** - Celery monitoring tool

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `SETTINGS` | Settings module | `production` |
| `POSTGRES_DB` | Database name | `devsearch_db` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | Required |
| `POSTGRES_HOST` | Database host | `localhost` |
| `EMAIL_HOST` | SMTP host | Required |
| `EMAIL_HOST_USER` | SMTP username | Required |
| `EMAIL_HOST_PASSWORD` | SMTP password | Required |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Required |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Required |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.projects

```

## Internationalization

The project supports English and French languages.

### Adding/Updating Translations

1. **Extract translatable strings**
```bash
python manage.py makemessages -l fr --ignore="venv/*"
```

2. **Edit translation files**
Edit files in [`locale/fr/LC_MESSAGES/django.po`](locale/fr/LC_MESSAGES/django.po)

3. **Compile translations**
```bash
python manage.py compilemessages
```

4. **Use Rosetta for web-based translation**
Access at `http://localhost:8000/rosetta/` (admin access required)

## API Endpoints

### Projects
- `GET /projects/` - List all projects ([`ProjectListView`](apps/projects/views.py))
- `GET /projects/<slug>/` - Project detail ([`ProjectDetailView`](apps/projects/views.py))
- `POST /projects/<slug>/` - Add review
- `GET /projects/add/` - Create project form
- `POST /projects/add/` - Create project
- `GET /projects/<slug>/edit/` - Edit project form
- `POST /projects/<slug>/edit/` - Update project
- `DELETE /projects/remove-tag/` - Remove tag from project

### Profiles
- `GET /profiles/` - List all profiles
- `GET /profiles/<username>/` - Profile detail
- `GET /account/` - User account dashboard

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/register/` - User registration
- `GET /accounts/verify-email/<token>/` - Email verification
- `POST /accounts/logout/` - User logout

## Screenshots

### Home Page
![Home Page](./static/images/Devsearch%20Home.jpg)

### Projects Page
![Projects Page](./static/images/DevSearch%20Projects.jpg)

### Profile Page
![Profile Page](./static/images/Devsearch%20Profile.jpg)

### User Inbox
![User Inbox](./static/images/Devsearch%20Inbox.jpg)

### Admin Login
![Admin Login](./static/images/devsearch-admin-login.png)

### Admin Dashboard
![Admin Dashboard 1](./static/images/devsearch-admin-dashboard-1.png)
![Admin Dashboard 2](./static/images/devsearch-admin-dashboard-2.png)


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## Troubleshooting

### Common Issues

**Database connection error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql
# Or with Docker
docker-compose ps
```

**Static files not loading**
```bash
python manage.py collectstatic --noinput
```

**Migrations conflict**
```bash
python manage.py makemigrations --merge
```

**Celery not processing tasks**
```bash
# Check Redis is running
redis-cli ping
# Restart Celery worker
celery -A dev worker -l info --pool=solo
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* Django community for the excellent framework
* All contributors who have helped shape this project

## Contact

Project Link: [https://github.com/praise002/devsearch](https://github.com/praise002/devsearch)

---

**Note**: This project is under active development. Features and documentation are subject to change.