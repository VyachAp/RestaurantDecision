import string
import secrets

alphabet = string.ascii_letters + string.digits


def generate_password():
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password
