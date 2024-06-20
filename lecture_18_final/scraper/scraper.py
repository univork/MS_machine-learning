from base64 import b64decode
from io import BytesIO
import logging
import os
from pathlib import Path
import re
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By


logging.basicConfig(encoding='utf-8', level=logging.INFO)

IMAGE_DOWNLOADER_SCRIPT = r"""
var img = document.getElementsByTagName("img")[0];
var canvas = document.createElement("canvas");
canvas.width = img.width;
canvas.height = img.height;
var ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0);
var dataURL = canvas.toDataURL("image/png");
return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
"""


class Scraper:
    search_emotions = ["happy", "sad"]
    output_path = Path(__file__).parent.parent / "data"

    def __init__(self) -> None:
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
    
    def quit(self):
        self.driver.quit()
    
    def get_image_links(self, url: str) -> list[str]:
        links = []
        number_of_scrolls = 1000
        self.driver.get(url)
        screen_height = self.driver.execute_script("return window.screen.height;")
        for i in range(1, number_of_scrolls + 1):
            logging.info("Scrolling page: %s - %s", i, number_of_scrolls)
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            time.sleep(1)

        elements = self.driver.find_elements(By.TAG_NAME, value="img")
        links.extend([
            element.get_attribute("src") \
            for element in elements \
            if not ".svg" in element.get_attribute("src") \
            and re.search(r"\/photos\/\d+", element.get_attribute("src"))
        ])

        return links
    
    def download_images(self, urls: list[str], output_path: str) -> None:
        for i, src in enumerate(urls):
            logging.info("Downloading image %s of %s", i+1, len(urls))
            self.driver.get(src)
            b64img = self.driver.execute_script(IMAGE_DOWNLOADER_SCRIPT) 

            # Decode from base64, translate to bytes and write to PIL image
            image_name = re.findall(r"\d{4,}", src)[0]
            img = Image.open(BytesIO(b64decode(b64img)))
            img.save(f"{output_path}/{image_name}.png")
    
    def setup_folder_structure(self):
        for emotion in self.search_emotions:
            os.makedirs(self.output_path / f"raw/{emotion}", exist_ok=True)
            os.makedirs(self.output_path / f"raw/{emotion}", exist_ok=True)

    def run(self):
        logging.info("Starting scraping...")
        self.setup_folder_structure()
        for emotion in self.search_emotions:
            logging.info("Scraping query %s person", emotion)
            image_links = self.get_image_links(f"https://www.pexels.com/search/{emotion} person")
            logging.info("Downloading %s images", len(image_links))
            self.download_images(image_links, output_path=self.output_path / f"raw/{emotion}")

        self.quit()


if __name__ == "__main__":
    Scraper().run()
