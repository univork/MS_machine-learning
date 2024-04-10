"""This module contains base scraper class for real estate data collection scrapers"""

import abc
from enum import Enum
import luigi  # type: ignore
import pandas as pd


DIRECTORY = "data"


class Website(Enum):
    """Website names"""

    SS = "ss"
    MYHOME = "myhome"


class Scraper(luigi.Task, abc.ABC):

    @property
    @abc.abstractmethod
    def website(self) -> Website:
        """scraped website"""
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self) -> list[dict]:
        """Execute the scraper"""
        raise NotImplementedError

    def report_progress(self, message: str, percentage: int) -> None:
        """update progress bar in luigi GUI interface"""
        if self.set_status_message is not None:
            self.set_status_message(message)  # pylint: disable=not-callable
            self.set_progress_percentage(percentage)  # pylint: disable=not-callable

    def output(self) -> luigi.LocalTarget:
        output_path = f"{DIRECTORY}/{self.website.value}.csv"
        return luigi.LocalTarget(output_path)

    def run(self) -> None:
        result = self.execute()
        df = pd.DataFrame([model.model_dump() for model in result])
        df.to_csv(self.output().path, index=False)
