import copy
import sys
from urllib import parse

import requests


def request(url):
    headers = {"User-Agent":
                   "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        pass


def is_vulnerable(html):
    errors = ["mysql_fetch_array()",
              "You have an error in your SQL syntax"]
    for error in errors:
        if error in html:
            return True


if __name__ == "__main__":
    url = sys.argv[1]
    url_parsed = parse.urlsplit(url)
    params = parse.parse_qs(url_parsed.query)
    for param in params.keys():
        query = copy.deepcopy(params)
        for c in "'\"":
            query[param][0] = c
            new_params = parse.urlencode(query, doseq=True)
            url_final = url_parsed._replace(query=new_params)
            url_final = url_final.geturl()
            html = request(url_final)
            if html:
                if is_vulnerable(html):
                    print("[ + ] {} parameter is vulnerable".format(param))
                    quit()

    print("NOT VULNERABLE")
