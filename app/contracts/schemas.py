import secrets

# Gera uma string hexadecimal aleatória de 32 bytes (64 caracteres hexadecimais)
# Isso é mais do que suficiente para uma SECRET_KEY segura.
secret_key = secrets.token_hex(32)
print(secret_key)