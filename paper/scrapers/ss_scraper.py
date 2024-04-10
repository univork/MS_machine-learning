"""This module contains scraper for https://home.ss.ge"""

import logging
from typing import Optional
import requests # type: ignore

from scrapers.property_details import PropertyDetails
from scrapers.scraper import Scraper, Website

logger = logging.getLogger(__name__)

URL = "https://api-gateway.ss.ge/v1/RealEstate/LegendSearch"
DETAIL_URL = "https://api-gateway.ss.ge/v1/RealEstate/details?applicationId={appid}&updateViewCount=true"
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
        response = self.request_with_token("https://api-gateway.ss.ge/v2/RealEstate/LegendSearchCount", "POST", payload)
        return response.json()["count"]

    def update_token(self) -> None:
        response = requests.get("https://home.ss.ge/ka/udzravi-qoneba/l/bina/iyideba?currencyId=1&page=1")
        self.token = response.cookies["ss-session-token"]

    def request_with_token(self, url, method: str, payload) -> Optional[requests.Response]:
        response = requests.request(method=method, url=url, headers={**HEADERS, "Authorization": f"Bearer {self.token}"}, json=payload)
        if response.status_code == 401:
            self.update_token()
            response = requests.request(method=method, url=url, headers={**HEADERS, "Authorization": f"Bearer {self.token}"}, json=payload)
        else:
            try:
                response.raise_for_status()
            except:
                return None
        return response

    def scrape_single_page(self, page: int) -> list[str]:
        response = self.request_with_token(URL, "POST", payload={**payload, "page": page})
        if response is None:
            return []

        links = [DETAIL_URL.format(appid=item["applicationId"]) for item in response.json()["realStateItemModel"] if item["applicationId"] != 0]
        return links

    def get_property_detail_links(self) -> list[dict]:
        approximate_pages = self.get_approximate_listings() / 30
        scraping = True
        page = 1
        links = []
        while scraping:
            page_properties = self.scrape_single_page(page)
            if len(page_properties) > 0:
                links.extend(page_properties)
                message = f"Step 1/2, collecting property links\nScraped: {page} of {int(approximate_pages)}"
                logger.info(message)
                self.report_progress(
                    message,
                    int(100 * page / approximate_pages)
                )
                page += 1
            else:
                scraping = False
                logger.info(f"No more properties on page {page}.")
        return links
    
    def get_property_details(self, url) -> PropertyDetails:
        response = self.request_with_token(url, "PUT", payload)
        if response is None:
            return None

        serialized_prop = PropertyDetails(**response.json())
        return serialized_prop

    def execute(self) -> list[PropertyDetails]:
        logger.info("SS scraper started!")
        links = self.get_property_detail_links()
        properties = []
        logger.info("Step 2/2...")
        for i, link in enumerate(links):
            prop = self.get_property_details(link)
            if prop is not None:
                properties.append(prop)
            else:
                logger.info("Failed request on %s", link)
            message = f"Collecting property details\nScraped: {i+1} of {len(links)}"
            logger.info(message)
            self.report_progress(
                "Step 2/2\n" + message,
                int(100 * i+1 / len(links))
            )
        return properties
    

if __name__ == "__main__":
    SSScraper().run()
