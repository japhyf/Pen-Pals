from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('dev')
    return serializer.dumps(email, salt='penpalsmf')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('dev')
    try:
        email = serializer.loads(
            token,
            salt='penpalsmf',
            max_age=expiration
        )
    except:
        return False
    return email
