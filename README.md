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

Notes:
- Pagination is not implemented for time-saving