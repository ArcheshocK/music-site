# Music Site - Django Web Application

This project is created for the [University of Helsinki Cyber Security Base 2025](https://cybersecuritybase.mooc.fi/) course project  
It demonstrates a simple music library web application written in Django. It is intentionally containing security flaws from the [OWASP Top 10 (2021)](https://owasp.org/Top10/).

---

## Features
- User authentication (login, logout and register)
- Browse available music files
- Download music
- Mark favorites
- Track user activity (downloads and favorites)
- Search for other users

## Existing Users
- username: alice | password: password123  
- username: bob   | password: password123  
- username: axel  | password: password123

---

## Security Flaws Demonstrated

### [Flaw 1: Broken Access Control (A01:2021)](https://github.com/ArcheshocK/music-site/blob/main/library/views.py#L40-L55)
- Any authenticated user can download any file, regardless of authorization.
- Suggested fix : add permission checks to restrict downloads to files authorized for the user.

### [Flaw 2: Sensitive Data Exposure (A04:2021)](https://github.com/ArcheshocK/music-site/blob/main/music_site/settings.py#L19-L23)
- The Django `SECRET_KEY` is hardcoded and visible in the repository
- In production, secrets should be stored in environment variables

### [Flaw 3: Cross-Site Request Forgery (A05:2021)](https://github.com/ArcheshocK/music-site/blob/main/templates/registration/login.html#L8-L14)
- Forms are vulnerable to CSRF if `{% csrf_token %}` is missing
- Fix (alredy active in code): CSRF token added to login form

### [Flaw 4: SQL Injection (A03:2021)](https://github.com/ArcheshocK/music-site/blob/main/library/views.py#L80-L103)
- Raw SQL query is executed with unsanitized user input
- suggested fix: use Django ORM (`User.objects.filter(...)`) or parameterized queries

### [Flaw 5: Security Misconfiguration (A05:2021)](https://github.com/ArcheshocK/music-site/blob/main/music_site/settings.py#L22-L26)
- `DEBUG = True` is enabled which exposes sensitive information if deployed in production
- Fix: set `DEBUG = False` in production

### [Flaw 6: Identification and Authentication Failures (A07:2021)](https://github.com/ArcheshocK/music-site/blob/main/music_site/settings.py#L1-L13) [(login.html)](https://github.com/ArcheshocK/music-site/blob/main/templates/registration/login.html#L3-L8)

- no rate limiting or lockout for repeated failed login attempts
- suggested fix: integrate `django-axes` to block brute force login attempts

---

## Installation & Running Locally

```bash
git clone https://github.com/ArcheshocK/music-site.git
cd music-site
python3 -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Visit http://127.0.0.1:8000 to access the site
