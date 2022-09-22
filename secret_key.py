import random
import string

secret_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))

print(secret_key)