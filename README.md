Practice project, only user management and auth logic is implemented
--------

**Before launch:**:
- Create ./keys directory
- Generate RSA private and public keys
- Place private key in ./keys/jwt.key
- Place public key in ./keys/jwt.key.pub
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
- Same for refresh token deactivation upon usage. Ideally, refresh token would contain token_id that would be tied to db entity (created for each refresh token, many to one to session). Once used, this db_entity would be marked as used. Upon repeated refresh token usage attempt, we would check that db_entity is used and reject. Currently, the same refresh token can be used unlimited amount of times until it is expired.