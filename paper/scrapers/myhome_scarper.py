"""This module contains scraper for https://myhome.ge"""

import requests
from scrapers.scraper import Scraper, Website

URL = "https://api2.myhome.ge/api/ka/search?Page={page}&CardView=2&slug[0]=yvela-gancxadeba"


class HyhomeScraper(Scraper):
    website = Website.MYHOME

    @staticmethod
    def get_approximate_pages() -> int:
        """returns number of pagination pages"""
        response = requests.get(URL.format(page=1))
        return response.json()["data"]["last_page"]
    
    def get_properties(self, page: int) -> list[dict]:
        """returns list of properties from given pagination page"""
        response = requests.get(URL.format(page=page))
        raw_properties = response["data"]["children"]
    
    def execute(self) -> list[dict]:
        pages = self.get_approximate_pages()
        all_properties = []
        for i in range(pages):
            page_properties = self.get_properties(i + 1)
            all_properties.extend(page_properties)
            self.report_progress(f"Scraped pages: {i+1} - {pages}", 100 * (i+1) / pages)
        return super().execute()
