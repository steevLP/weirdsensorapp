import requests

def dl(p,n):
    r = requests.get(p, allow_redirects=False)
    open(n, 'wb').write(r.content)