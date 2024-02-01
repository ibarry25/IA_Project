from cryptography.fernet import Fernet

def dechiffrement(encrypted_message, cle):
    cipher_suite = Fernet(cle)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# Exemple d'utilisation :
KEY = 'QiwlcwZnLtK8aK4LGl9wXwPs7OyHmfmv_ZOHe5vIXso='
CODE = b'gAAAAABlu-NXzP75wjUHZBKOFL2QEdBHpDWz76uy1uVhTZHGSZD0YwEDjiFm6qf_5EaiClvWvBzmHAcbyN7gYCncVt871esEaxO9IOUBKXoLz5tpicrEWZoJmXzwmHVWL8CYaAVvIzsUvLlGZ_ujQDxXdjzvNXPVl1Ui_I1b-VLJFvg5bP7HufE='

# Déchiffrement
TOKEN = dechiffrement(CODE, KEY)
