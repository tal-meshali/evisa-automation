import re

from visa_requests.stages.stage import Stage
from datetime import datetime, timedelta
from typing import List

DATE_REGEX = r"\d{2}\/\d{2}\/\d{4}"


class FixUnknownDate(Stage):
    def run(self, stage_input: str):
        return stage_input.replace("00", "01")


class CreateDateStage(Stage):
    def __init__(self, _format: str, should_loop: bool = False):
        self._format = _format
        super().__init__(should_loop)

    def run(self, stage_input: str):
        return datetime.strptime(stage_input, self._format)


class AddDaysToDateStage(Stage):
    def __init__(self, amount_of_days: int, should_loop: bool = False):
        self.amount_of_days = amount_of_days
        super().__init__(should_loop)

    def run(self, stage_input: datetime):
        return stage_input + timedelta(days=self.amount_of_days)


class ConvertDateToISOStage(Stage):
    def run(self, stage_input: datetime):
        return stage_input.isoformat() + ".000Z"


class ConvertDateToRegularStage(Stage):
    def run(self, stage_input: datetime):
        return stage_input.strftime("%d/%m/%Y")


class AcquireAllDatesStage(Stage):
    def run(self, stage_input: List[str]):
        return filter(lambda word: re.match(DATE_REGEX, word), stage_input)


class SortDatesStage(Stage):
    def run(self, stage_input: List[datetime]):
        return sorted(set(stage_input))[:3]
