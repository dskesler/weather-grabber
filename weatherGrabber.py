import requests
from bs4 import BeautifulSoup
import re
from os import listdir


class WeatherGrabber:
    urls = []
    results = []

    def __init__(self, url: str, **kwargs):
        if kwargs is not None:
            self.image_pattern = kwargs.get('img_pattern')
            self.url_pattern = kwargs.get('url_pattern')
            response = requests.get(url)
            self.html_parser = BeautifulSoup(response.content, 'html.parser')

    def get_html_parser(self):
        return self.html_parser

    def set_urls(self):
        for link in self.html_parser.find_all('a'):
            href = link.get('href')
            if re.search(self.url_pattern, href) and href not in self.urls:
                self.urls.append(href)

    def set_results(self):
        for u in self.urls:
            r = requests.get(u)
            page = BeautifulSoup(r.content, 'html.parser')
            for i in page.find_all('img'):
                img_text = i['src']

                # print(imgText)
                if re.match(self.image_pattern, img_text):
                    self.results.append(re.sub('-600x298', '', img_text))  # removing smaller resolution portion of url

    def write_images_to_files(self):
        path = "."
        file_list = [f for f in listdir(path)]
        for result in self.results:
            img = requests.get(result)
            file_name = result.rsplit('/', 1)[1]
            if file_name not in file_list:
                (file_name, 'wb').write(img.content)


def run():
    url = 'https://www.alabamawx.com'
    img_pattern = re.compile(r'.*gfs-KBHM-daily_tmin_tmax.*')
    url_pattern = re.compile(r'https:\/\/www.alabamawx.com\/\?p=\d+')
    wb = WeatherGrabber(url, img_pattern=img_pattern, url_pattern=url_pattern)
    wb.set_urls()
    print(*wb.urls, sep='\n')
    wb.set_results()
    wb.write_images_to_files()


if __name__ == "__main__":
    run()
