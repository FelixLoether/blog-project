from getpass import getpass

while True:
    username = raw_input('Enter desired username: ')

    if username:
        break

while True:
    pwd1 = getpass('Enter password: ')
    pwd2 = getpass('Re-enter password: ')

    if pwd1 == pwd2:
        password = pwd1
        break

import blog
blog.install(username, password)
