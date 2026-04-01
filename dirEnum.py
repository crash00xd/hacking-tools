import requests

url = "INSIRA DO DOMÍNIO"

with open("wordlist.txt", "r") as file:
	wordlist = file.readline()

for word in wordlist:
	url_final = "{}/{}".format(url, word.strip())
	response = requests.get(url_final)
	code = response.status_code
	if code != 404:
		print("{} -- {}".format(url_final, code))
