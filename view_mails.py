import requests

EMAIL = []

for i in range(50):
    response = requests.get("http://shop.bancocon.com/rest/products/{}/reviews".format(i))
    data_json = response.json()
    for view in data_json["data"]:
        if email not in EMAILS:
            print(view["author"])
            EMAILS.append(email)
