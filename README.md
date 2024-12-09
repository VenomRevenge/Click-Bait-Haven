# ClickBait Haven

A dynamic journalism web app allowing users to publish, review, and interact with articles. Designed with user roles and permissions for a secure and efficient experience.

---

## General Requirements
- **Python**: Version 3.11.1 or higher  
- **PostgreSQL**: Database
- **pip**: For installing dependencies  
- **Browser**: Developed and tested using Brave and Chrome. A Chromium-based browser is recommended but others probably work as well.
- **GIT**: Alternatively you can just download the source code.
---

## Setup Instructions

### Step 1: Clone the project
```bash
git clone https://github.com/VenomRevenge/Click-Bait-Haven.git
```
And navigate to the root directory (manage.py level)
 ```bash
cd Click-Bait-Haven
```

### Step 2: Install Dependencies


Run the following command to install required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 3: Create a `.env` File
At the root level of the project (where `manage.py` is located), create a `.env` file using this template:
```env
# Django secret key
# You dont need to set this or change it if you are testing
# you can read the comment in the settings.py if you are wondering
# why I left it here
SECRET_KEY="django-insecure-zlv-0v4xsdk5&ppexf6ndep&1pm%%3-r59mk-xfckdq+y$b-wu"

# Debug mode
DEBUG="True"  # Set to "False" for production

# PostgreSQL database settings
DB_NAME="your_db_name"
DB_USER="postgres"  # or your PostgreSQL username
DB_PASSWORD="your_postgres_user_password"
DB_HOST="127.0.0.1" # or your host
DB_PORT="5432" # or your port

# Web3Forms API key for testing contact email feature
WEB3FORMS_EMAIL_ACCESS_KEY="your_key_here"
```

### Step 4: Database Migration
Run the following command to apply migrations:
```bash
python manage.py migrate
```

### Step 5: Load Testing Data
Use this command to load pre-generated test data:
```bash
python manage.py loaddata data.json
```

**Note**: It is recommended to use a freshly created database for optimal results.

---

## User Roles and Permissions

The web app features six types of users, each with unique permissions:

### 1. Anonymous Users
- View and search articles.
- Register and sign in.

### 2. Citizen Journalists (regular users without permissions)
- All anonymous user permissions.
- Publish articles (subject to review).
- Edit profile and articles (articles return to the review phase upon edits).
- Comment on and react to articles/comments.
- Delete their profile (permanently) or articles (soft delete).
- Receive notifications for article reviews.

### 3. Confirmed Journalists (users with the profiles.confirmed_journalist permissions)
- All citizen journalist permissions.
- Bypass article review phases (including after edits).

### 4. Moderators  (users with the profiles.moderator permissions )
- All confirmed journalist permissions.
- Review articles and notify authors.
- Access the article review page for unreviewed articles.

### 5. Staff
- All moderator permissions.
- Permanently ban users.
- Access the Django admin site.

### 6. Superuser
- All staff permissions.
- Full CRUD on all users, articles, and comments.
- Access soft-deleted articles for reinstatement or permanent deletion.

---

## Testing User Accounts

Pre-generated user accounts are provided for testing purposes:

| Role                 | Username         | Email                   | Password    |
|----------------------|------------------|-------------------------|-------------|
| Superuser            | ClickBaitAdmin  | clickbaitadmin@gmail.com | 12admin34   |
| Staff                | ClickBaitStaff  | clickbaitstaff@gmail.com | 12staff34   |
| Moderator            | plamen          | plamen@gmail.com         | 12plamen34  |
| Confirmed Journalist | John            | john@gmail.com           | 12john34    |
| Regular User         | ivan            | ivan@gmail.com           | 12ivan34    |

---

## Features

### General Features
- **Login**: Supports both username and email authentication.
- **Dynamic Homepage**: Displays featured and recent articles.
- **Article Search**: Advanced filtering options.
- **Pagination**: Available on multiple pages.
- **Markdown Support**: Styled article content with sanitized inputs using the `bleach` library.

### Security
- Secure permissions with custom helpers and wrappers.
- Input sanitization to prevent injection or malicious exploits.
- User-uploaded images (profile and article) are validated and resized.

### Notifications
- Displays unread notifications in the header.
- Notifies users when their articles are reviewed.
- Notifies users with permissions to review articles.

### API Endpoints
- **`api/articles/`**: Fetch and filter articles.  
- **`api/article/<id>/`**: Fetch a single article's details.  
- **`api/tags/`**: Fetch all available article tags.  

API documentation is available at `/api/` with Swagger UI.

### Custom Admin Site
- Built with Django Unfold for enhanced admin features:
  - Manage user roles and permissions en masse.
  - Advanced filtering and search options.
  - CRUD operations on users, groups, profiles, articles, comments, and tags.

### Asynchronous Contact Form
- Implements Web3Forms for email-based communication with the site owner.

**Note**: Visit https://web3forms.com/ to get your key, its free and no registration required.

