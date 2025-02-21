import bcrypt

password1 = "mypassword"
password2 = "mypassword"
# Generate a unique salt

# Hash the password with the salt
hashed_password1= bcrypt.hashpw(password1.encode(), bcrypt.gensalt())
hashed_password2 = bcrypt.hashpw(password2.encode(),bcrypt.gensalt())
print("Hashed Password 1:", hashed_password1)
print("Hashed Password 2:", hashed_password2)
