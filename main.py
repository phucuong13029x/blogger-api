from app import *
from app._config import fd_data, url
from app._process import _readtxt, _create_content
from app._blogger import blogger_sdk


blogger = blogger_sdk(id='4691855219075129795')

if __name__ == "__main__":
    while True:
        url = url
        main = BeautifulSoup(requests.get(url).text, 'html.parser')
        list_post = []
        list_post.extend(main.select("* article div.z-txt a"))
        list_post.extend(main.select("* article div.z-foto a"))
        list_href_new = []
        for i in list_post:
            href = i.get("href")
            if str(href)[:1] == "/":
                list_href_new.append(i.get("href"))
        list_href_old = _readtxt(fd_data + os.sep + "list.txt")
        list_href = set(list_href_new) ^ set(list_href_old)
        if list_href:
            for i in list_href:
                url_href = f"{url}{i}"
                title, content, meta, labels = _create_content(url=url_href)
                ports = blogger._create_post(title=title,content=content, meta=meta, labels=labels)
                print(ports)
                break
        time.sleep(1000)
                