import logging
import luigi # type: ignore
import pandas as pd

from scrapers.scraper import Scraper, DIRECTORY
from scrapers.ss_scraper import SSScraper

logging.basicConfig(filename="logs.log", filemode="a", level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Writer(luigi.Task):

    def requires(self) -> list[Scraper]:
        return [SSScraper()]

    def output(self):
        return luigi.LocalTarget(f"{DIRECTORY}/real_estate.csv")
    
    def run(self) -> None:
        dfs = []
        for i, scraper in enumerate(self.input()):
            logger.info("Parsing %s", i+1)
            df = pd.read_csv(scraper.path, index_col=False)
            dfs.append(df)

        full_df = pd.concat(dfs, ignore_index=True)
        full_df.to_csv(self.output().path, index=False)
