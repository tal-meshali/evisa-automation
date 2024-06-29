import re

from ..stages.stage import Stage
from typing import List
from ..validators.string_matcher import ProximityChecker

VALID_CHARACTERS_ONLY = r"[a-zA-Z01\s]+"


class ScannedStringStage(Stage):
    def run(self, stage_input):
        return (
            stage_input.replace("$", "S")
            .replace("1", "I")
            .replace("0", "O")
            .strip("<")
            .strip()
        )


class FilterValidWordsOnlyStage(Stage):
    def run(self, stage_input: List[str]):
        return list(
            filter(lambda word: re.match(VALID_CHARACTERS_ONLY, word), stage_input)
        )


def connect_words(word_list: List[str]):
    if len(word_list) == 1:
        return word_list[0]
    return word_list[0] + " " + connect_words(word_list[1:])


class StringFieldMatchStage(Stage):
    def __init__(self, field_definition: List[str], definition_threshold: int):
        self.field_definition = field_definition
        self.definition_checker = ProximityChecker(
            connect_words(self.field_definition), definition_threshold
        )
        self.checking_length = len(self.field_definition)

    def run(self, stage_input: List[str]):
        while len(stage_input) > self.checking_length:
            scanned_string = stage_input[: self.checking_length]
            if self.definition_checker.run(connect_words(scanned_string)):
                return stage_input[self.checking_length :]
            stage_input = stage_input[1:]
        return False


class FindResultUntilStopWordStage(Stage):
    def __init__(self, stop_word: str, stop_threshold: int):
        self.stop_word_checker = ProximityChecker(stop_word, stop_threshold)

    def run(self, stage_input: List[str]):
        words_required: List[str] = []
        for word in stage_input:
            if self.stop_word_checker.run(word):
                return connect_words(words_required)
            words_required.append(word)


class GetFirstWordStage(Stage):
    def run(self, stage_input: List[str]):
        return stage_input[0]
