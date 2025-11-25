# Secure Vulpy – Hardened Web Application

## Project Overview

Secure Vulpy is a security-enhanced version of the intentionally vulnerable *Vulpy* application. This project demonstrates secure coding practices by identifying and fixing common web vulnerabilities such as SQL injection, CSRF, XSS, insecure session handling, IDOR, and weak role-based access control.

The primary goal is to implement and document security improvements as required for the CA2 Secure Web Development assessment.

---

## Features & Security Objectives

### Core Application Features

* User registration and login
* MFA support
* User profile pages
* Post creation
* Admin dashboard (view all users)
* Password management

### Security Enhancements Implemented

* **SQL Injection Prevention** – Parameterized queries across the application
* **CSRF Protection** – Per-session token creation and server-side validation
* **Secure Session Handling** – Full session dict stored with HttpOnly + SameSite cookies
* **Password Hardening** – bcrypt hashing with migration script
* **Cross-Site Scripting (XSS) Mitigation** – Input sanitization + strict CSP
* **IDOR Protection** – Only admin can view other user’s posts
* **Role-Based Access Control (RBAC)** – Admin/user privilege separation
* **Security Headers** – CSP, X-Frame-Options, Referrer-Policy, X-Content-Type-Options

---

## Project Structure

```
project/
│
├── good/                      # Core secure application code
│   ├── vulpy.py                # Flask entry point
│   ├── libsession.py         # Secure session management
│   ├── libuser.py            # Auth + bcrypt + safe queries
│   ├── libposts.py           # Safe post handling
│   ├── libcsrf.py            # CSRF token management
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, fonts, images
│   └── db_users.sqlite       # SQLite DB 
│
├── scripts/
│   └── hash_passwords.py     # Password migration to bcrypt
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your_repo_url>
cd secure-vulpy
```

### 2. Create & activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\\Scripts\\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize database (optional)

```bash
python bad/scripts/db_init.py      # Initialize DB (if missing)
python scripts/hash_passwords.py   # Migrate plaintext passwords → bcrypt
```

### 5. Run the application

```bash
python bad/app.py
```

### 6. Access in browser

```
http://127.0.1.1:5000
```

---

## Usage Guide

### Register & Login

* Create an account at **/user/create**
* Login via **/user/login**
* MFA (if enabled) prompts for OTP

### Create Posts

* Navigate to `/posts/<username>`
* Use CSRF-protected form to submit posts

### Admin Dashboard

* Login as admin
* Visit `/posts/admin`
* View all user profiles/posts (RBAC enforced)

### Change Password

* Navigate to `/user/chpasswd`
* bcrypt-secured update

---

## Security Improvements (Summary)

### 1. SQL Injection Prevention

* Parameterized queries in `libuser.py` and `libposts.py`

### 2. CSRF Protection

* Per-session `_csrf` tokens
* Hidden input fields in all POST forms
* Server-side validation on each POST request

### 3. Session Security

* Entire session dictionary stored securely
* HttpOnly + SameSite cookie flags

### 4. XSS Mitigation

* Sanitized output
* Removed unsafe `|safe`
* Strong Content Security Policy applied

### 5. Password Hardening

* bcrypt hashing
* Included migration script for legacy plaintext passwords

### 6. RBAC & IDOR Fixes

* Admin-only access to sensitive areas
* Regular users cannot view others' posts

### 7. Security Headers

* CSP
* X-Frame-Options
* Referrer-Policy
* X-Content-Type-Options

---

## Testing Overview

### Manual Testing

* SQLi payloads (`' OR '1'='1`)
* XSS payloads (`<script>alert(1)</script>`)
* CSRF bypass attempts (curl, altered tokens)
* Session tampering tests
* IDOR tests (`/posts/<otheruser>` as non-admin)

### Key Findings

* All major vulnerabilities mitigated successfully
* No critical findings after fixes
* Application follows secure development principles

---

## Contributions & References

* Vulnerable Vulpy: [https://github.com/fportantier/vulpy](https://github.com/fportantier/vulpy)
