from ..information.attribute import Attribute
from ..pipelines.dates import PassportDatePipeline
from ..pipelines.strings import SurnamePipeline, GivenNamePipeline, BirthPlacePipeline
from ..pipelines.passport_number import PassportNumberPipeline
from ..pipelines.general import ReceiveRequiredDatesPipeline, InitialWordListPipeline
from typing import List, Dict


class SimplePassportFiller:
    def __init__(self):
        self.birth_date = Attribute(PassportDatePipeline(), ["birth_date"])
        self.last_name = Attribute(SurnamePipeline(), ["last_name"])
        self.first_name = Attribute(GivenNamePipeline(), ["first_name"])
        self.birth_place = Attribute(BirthPlacePipeline(), ["birth_place"])
        self.passport_number = Attribute(PassportNumberPipeline(), ["passport_number"])
        self.issue_date = Attribute(PassportDatePipeline(), ["issue_date"])
        self.expiry_date = Attribute(PassportDatePipeline(), ["expiry_date"])
        self.dates_pipeline = ReceiveRequiredDatesPipeline()
        self.words_pipeline = InitialWordListPipeline()

    def fill_in_details(self, word_list: List[str], result_dictionary: Dict):
        self.fill_in_dates(word_list, result_dictionary)
        word_list = self.words_pipeline.activate(word_list)
        self.last_name.update(word_list, result_dictionary)
        self.first_name.update(word_list, result_dictionary)
        self.birth_place.update(word_list, result_dictionary)
        self.passport_number.update(word_list, result_dictionary)

    def fill_in_dates(self, word_list: List[str], result_dictionary: Dict):
        birth_date, issue_date, expiry_date = self.dates_pipeline.activate(word_list)
        self.birth_date.update(birth_date, result_dictionary)
        self.issue_date.update(issue_date, result_dictionary)
        self.expiry_date.update(expiry_date, result_dictionary)
