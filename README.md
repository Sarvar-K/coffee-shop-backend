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

Functionality extension:
- Group new database models by their meaning and place them in appropriately named modules. Place those modules in _src.models_ package.
- Place functions that perform Create/Retrieve/Update/Delete (CRUD) operations on database models in _src.crud_ package. Name modules respective to their models modules.
- Place pydantic schemas for request/response serialization and validation in _src.schemas_ package
- Place functions that perform logic operations in _src.core_ package
- Place new routers in _src.api.routers_ module
- Place new endpoints in modules named after their respective router component and place those modules in _src.api.v1.endpoints_ package

Notes:
- Pagination is not implemented for time-saving
- Same for repeated otp code request. Otp code can be requested once during signup.
- Same for refresh token deactivation upon usage. Ideally, refresh token would contain token_id that would be tied to db entity (created for each refresh token, many to one to session). Once used, this db_entity would be marked as used. Upon repeated refresh token usage attempt, we would check that db_entity is used and reject. Currently, the same refresh token can be used unlimited amount of times until it is expired.