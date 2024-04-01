
"""This module contains scraper for https://home.ss.ge"""

import logging
import requests # type: ignore
import pandas as pd

from scrapers.scraper import Scraper, Website

logger = logging.getLogger(__name__)

URL = "https://api-gateway.ss.ge/v1/RealEstate/LegendSearch"
HEADERS = {
    "Origin": "https://home.ss.ge",
    "Referer": "https://home.ss.ge/",
    "User-Agent": "Mozilla/5.0"
}
payload = {
    "currencyId": 1,
    "page": 1,
    "pageSize": 30,
    "realEstateDealType": 4,
    "realEstateType": 5,
}


class SSScraper(Scraper):
    website = Website.SS

    def __init__(self) -> None:
        super().__init__()
        self.update_token()
    
    def get_approximate_listings(self) -> int:
        response = self.post_with_token("https://api-gateway.ss.ge/v2/RealEstate/LegendSearchCount", payload)
        return response.json()["count"]

    def update_token(self) -> None:
        response = requests.get("https://home.ss.ge/ka/udzravi-qoneba/l/bina/iyideba?currencyId=1&page=1")
        self.token = response.cookies["ss-session-token"]

    def post_with_token(self, url, payload) -> requests.Response:
        response = requests.post(url, headers={**HEADERS, "Authorization": f"Bearer {self.token}"}, json=payload)
        if response.status_code == 401:
            self.update_token()
            response = requests.post(URL, headers={**HEADERS, "Authorization": f"Bearer {self.token}"})
        else:
            response.raise_for_status()

        return response

    def scrape_single_page(self, page: int):
        response = self.post_with_token(URL, payload={**payload, "page": page})
        
        properties = []
        parsed_response = response.json()
        for prop in parsed_response["realStateItemModel"]:
            title = prop["title"]
            address = prop["address"]
            price = prop["price"]
            total_area = prop["totalArea"]
            building_floors = prop["totalAmountOfFloor"]
            floor = prop["floorNumber"]
            bedrooms = prop["numberOfBedrooms"]

            prop_norm = {
                "title": title,
                "address": address,
                "price": price,
                "total_area": total_area,
                "total_floors": building_floors,
                "floor": floor,
                "bedrooms": bedrooms

            }
            properties.append(prop_norm)
        return properties


    def execute(self) -> list[dict]:
        approximate_pages = self.get_approximate_listings() / 30
        scraping = True
        page = 1
        properites = []
        while page<5:
            page_properties = self.scrape_single_page(page)
            if len(page_properties) > 0:
                properites.extend(page_properties)
                self.report_progress(f"Scraped: {page} of {approximate_pages}", int(100 * page / approximate_pages))
                page += 1
            else:
                scraping = False
                print(f"No more properties on page {page}.")
                print("DONE!")
        return properites
    

if __name__ == "__main__":
    SSScraper().run()
    # df = pd.DataFrame(properies)
    # df.to_csv("./real_estate.csv", index=False)
