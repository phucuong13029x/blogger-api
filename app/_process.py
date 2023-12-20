from app import *


def _create_content(url):
    try:
        trs = _translator()
        response   = requests.get(url)
        main       = BeautifulSoup(response.text, 'html.parser')
        article    = main.find("article", {"class":"main-article"})
        gr_title   = article.find("hgroup", {"class":"zona-titulo"})
        gr_content = article.find("div", {"id":"cuerpo-nota"})
        gr_labels  = article.find("div", {"class":"tags-group"})
        gr_labels  = gr_labels.select("a")

        title      = gr_title.find("h1", {"class":"titular"}).text
        title      = trs._translator(title, 'en')

        meta       = gr_title.find("strong", {"class":"bajada"}).text
        meta       = trs._translator(meta, 'en')

        labels     = gr_title.find("h2", {"class":"volanta"}).text
        labels     = [trs._translator(labels, 'en')]

        thumbnail  = (article.find("div", {"class":"my-gallery main-gallery"})).find("img")
        thumbnail_alt = thumbnail.get('alt')
        thumbnail_data = _image(f"https://www.panoramaweb.com.mx{thumbnail.get('src')}")
        thumbnail_convert = f"<table align='center' cellpadding='0' cellspacing='0' class='tr-caption-container' style='margin-left: auto; margin-right: auto;'><tbody><tr><td style='text-align: center;'><img alt='{thumbnail_alt}' src='{thumbnail_data}' title='{thumbnail_alt}' width='100%' /></td></tr><tr><td class='tr-caption' style='text-align: center;'>{thumbnail_alt}</td></tr></tbody></table>"
        
        content = str(thumbnail_convert)
        for i in gr_content:
            if i.name in ['p','h1','h2']:
                text = i.text
                text = trs._translator(text, 'en')
                if i.name == 'p':
                    content += f"<p>{text}</p>"
                elif i.name == 'h1':
                    content += f"<h1>{text}</h1>"
                elif i.name == 'h2':
                    content += f"<h2>{text}</h2>"
            if i.name == "figure":
                alt_img  = ""
                data_img = ""
                meta_img = i.text
                for j in i:
                    if j.name == "img":
                        src_img  = f"https://www.panoramaweb.com.mx{j.get('src')}"
                        alt_img  = j.get('alt')
                        data_img = _image(src_img)
                img_convert  = f"<table align='center' cellpadding='0' cellspacing='0' class='tr-caption-container' style='margin-left: auto; margin-right: auto;'><tbody><tr><td style='text-align: center;'><img alt='{alt_img}' src='{data_img}' title='{alt_img}' width='100%' /></td></tr><tr><td class='tr-caption' style='text-align: center;'>{meta_img}</td></tr></tbody></table>"
                content += img_convert
            if i.name == 'ul':
                retext = ""
                ls = i.select('li')
                for j in ls:
                    text = j.text
                    text = trs._translator(text, 'en')
                    j.replace_with(text)
                    retext += str(j)
                i.replace_with(retext)
                content += str(i)

        tags = ""
        for h in gr_labels:
            print(h)
            text1 = trs._translator(h.text, "en")
            text2 = str(text1).lower().replace(" ","-")
            a_html = f"<a href='/search?q={text2}' title='{text1}'>#{text2}</a>"
            print(a_html)
            tags+=a_html
        content += f"<br><br><p>Tags: {tags}</p>"
        return title, content, meta, labels
    except Exception as e:
        print(e)
        return False

class _translator:
    def __init__(self):
        self.conn = Translator()

    def _translator(self, content, language):
        result = self.conn.translate(content, dest=language)
        print(result)
        return result.text

def _image(url):
    try:
        params = {
            'expiration': '600',
            'key': '93efdc1169db8861b5bb47f48e363778',
        }
        files = {
            'image': (None, url),
        }
        response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
        return response.json()['data']['url']
    except Exception as e:
        print(e)
        return False

def _basedir():
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.getcwd()
    return path

def _readtxt(file_path):
    data = []
    if os.path.isfile(file_path) is True:
        with open(file_path, 'r', encoding='utf8') as f:
            for i in f.readlines():
                data.append(i.replace('\n',''))
            return data
    else:
        return data
    
def _writetxt(path, data):
    try:
        with open(path, "a+", encoding = "utf8") as f:
            f.seek(0)
            fdata = f.read(100)
            if len(fdata) > 0:
                f.write("\n")
            if type(data) == dict:
                f.write("\n".join(data))
            elif type(data) == str:
                f.write(data)
        return True
    except OSError as e:
        return False
