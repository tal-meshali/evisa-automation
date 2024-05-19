import re

from collections import Counter
from visa_requests.stages.stage import Stage
from typing import List

PASSPORT_NUMBER_REGEX = r"\d{8}"


class PassportNumberOptionsStage(Stage):
    def run(self, stage_input: List[str]):
        return filter(lambda word: re.match(PASSPORT_NUMBER_REGEX, word), stage_input)


class FindMostProbableOptionStage(Stage):
    def run(self, stage_input: List[str]):
        most_common_number = Counter(stage_input).most_common(1)[0]
        if most_common_number[1] == 2:
            return most_common_number[0]
        return list(filter(lambda passport_num: passport_num[0] in ["2", "3"], stage_input))[0]
