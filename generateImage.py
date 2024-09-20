import requests
from bs4 import BeautifulSoup
from io import BytesIO
import requests 
from PIL import ImageTk, Image
import sys
import os

class UrlGen():
    def __init__(self):
        base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.urls = open(os.path.join(base_dir, 'EL1Imgs.txt'), 'r').readlines()
        self.words = open(os.path.join(base_dir, 'EL1vocab.txt'), 'r').readlines()

    def getImage(self, words):
        image_urls = []
        for i in range(len(words)):
            image_urls.append(self.urls[self.words.index(words[i] + '\n')].replace('\n', ''))
        return image_urls

def getImage(words):
    image_urls = []
    for word in words:
        query = word + " clipart"  # the search query you want to make
        url = f"https://www.google.com/search?q={query}&tbm=isch"  # the URL of the search result page
        response = requests.get(url)  # make a GET request to the URL
        soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
        # find the first image link by searching for the appropriate tag and attribute
        img_tag = soup.find("img", {"class": "yWs4tf"})
        if img_tag is not None:
            img_link = img_tag.get("src")
            image_urls.append(img_link)
        else:
            print("No image found on the page.")
    return image_urls
"""
if __name__ == '__main__':
    words = []
    with open("EL1vocab.txt",'r') as data_file:
        for line in data_file:
            words.append(line.replace('\n', ''))
    print(words)
    urls = getImage(words)
    print(urls)
    with open('EL1Imgs.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')
"""