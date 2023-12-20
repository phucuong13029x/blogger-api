from app._process import os, _basedir


basedir = _basedir()
fd_data = basedir + os.sep + "data"
os.makedirs(fd_data, exist_ok=True)
authen = {
    "key": "AIzaSyCjUJmp_1lDCxINyP34qwvGtbKij29zgqk",
    "cer": f"{fd_data}/credentials.json",
    "token": f"{fd_data}/token.json"
}
url = "https://www.panoramaweb.com.mx"
