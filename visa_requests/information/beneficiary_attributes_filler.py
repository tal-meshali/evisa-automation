from visa_requests.information.attribute import Attribute
from visa_requests.pipelines.dates import ArrivalDatePipeline, DepartureDatePipeline, PassportDatePipeline, ReceiveRequiredDatesPipeline
from visa_requests.pipelines.strings import SurnamePipeline, GivenNamePipeline, BirthPlacePipeline, InitialWordListPipeline
from visa_requests.pipelines.passport_number import PassportNumberPipeline
from visa_requests.pipelines.profession import ReceiveProfessionPipeline
from typing import List, Dict

class BeneficiaryAttributesFiller:
    def __init__(self):
        self.birth_date = Attribute(PassportDatePipeline(True),
                                    ["refInfoBeneficiairesVisa", "dateNaissance"])
        self.last_name = Attribute(SurnamePipeline(),
                                   ["refInfoBeneficiairesVisa", "nom"])
        self.first_name = Attribute(GivenNamePipeline(),
                                    ["refInfoBeneficiairesVisa", "prenom"])
        self.birth_place = Attribute(BirthPlacePipeline(),
                                     ["refInfoBeneficiairesVisa", "lieuNaissance"])
        self.passport_number = Attribute(PassportNumberPipeline(),
                                         ["refInfoPasseport", "numPasseport"])
        self.profession = Attribute(ReceiveProfessionPipeline(),
                                    ["refInfoBeneficiairesVisa", "refProfession"])
        self.issue_date = (Attribute(PassportDatePipeline(True),
                                     ["refInfoPasseport", "dateDelivrance"]),
                           Attribute(PassportDatePipeline(False),
                                     ["dateDelivrPass"]))
        self.expiry_date = (Attribute(PassportDatePipeline(True),
                                      ["refInfoPasseport", "dateExpiration"]),
                            Attribute(PassportDatePipeline(False),
                                      ["dateExpirPass"]))
        self.travel_dates = (Attribute(ArrivalDatePipeline(True),
                                       ["dateArrivee"]),
                             Attribute(ArrivalDatePipeline(False),
                                       ["dateArrivePrevue"]),
                             Attribute(DepartureDatePipeline(True),
                                       ["dateSortie"]),
                             Attribute(DepartureDatePipeline(False),
                                       ["dateSortiePrevue"]))
        self.dates_pipeline = ReceiveRequiredDatesPipeline()
        self.words_pipeline = InitialWordListPipeline()

    def fill_in_details(self, word_list: List[str], result_dictionary: Dict, arrival_date: str):
        self.fill_in_dates(word_list, result_dictionary)
        word_list = self.words_pipeline.activate(word_list)
        self.last_name.update(word_list, result_dictionary)
        self.first_name.update(word_list, result_dictionary)
        self.birth_place.update(word_list, result_dictionary)
        for attribute in self.travel_dates:
            attribute.update(arrival_date, result_dictionary)

    def fill_in_dates(self, word_list: List[str], result_dictionary: Dict):
        birth_date, issue_date, expiry_date = self.dates_pipeline.activate(word_list)
        self.birth_date.update(birth_date, result_dictionary)
        for attribute in self.issue_date:
            attribute.update(issue_date, result_dictionary)
        for attribute in self.expiry_date:
            attribute.update(expiry_date, result_dictionary)
        self.profession.update(birth_date, result_dictionary)
