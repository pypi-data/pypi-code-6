from highfield.helpers.random import unique_id

session_cookie_name = 'HFSESS'
session_secret_key = unique_id(24)

csrf_token_lifespan = 18000
