Practice project, only user management and auth logic is implemented
--------

**Before launch:**:
- Create ./keys directory
- Generate private JWT key and place it in ./keys/jwt.key
- Generate public JWT key and place it in ./keys/jwt.key.pub
- Create .env and populate it according to .env_example

**Launch without containerization:**
```commandline
gunicorn
```

**Launch with containerization:**
```commandline
docker compose up -d
```

**Stop and remove launched containers:**
```commandline
docker compose down
```

**Generate migrations:**
```commandline
alembic revision --autogenerate -m "title"
```
Replace "title" with descriptive title for what migration changes. The -m flag is required.

**Apply migrations:**
```commandline
alembic upgrade head
```

Notes:
- Pagination is not implemented for time-saving
- Same for repeated otp code request. Otp code can be requested once during signup.