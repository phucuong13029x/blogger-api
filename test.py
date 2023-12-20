import requests

params = {
    'expiration': '600',
    'key': '93efdc1169db8861b5bb47f48e363778',
}
files = {
    'image': (None,"https://www.panoramaweb.com.mx/u/fotografias/m/2023/12/14/f768x1-65500_65627_15.jpg"),
}
response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
print(response.json())
print(response.json()['data']['url'])