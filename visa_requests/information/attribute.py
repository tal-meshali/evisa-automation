from visa_requests.pipelines.pipeline import Pipeline
from typing import List, Dict


class Attribute:
    def __init__(self, pipeline: Pipeline, path_to_save: List[str]):
        self.pipeline = pipeline
        self.path_to_save = path_to_save

    def update(self, raw_input, result_dictionary: Dict):
        current_location_dictionary = result_dictionary
        for path_section in self.path_to_save[:-1]:
            current_location_dictionary = current_location_dictionary[path_section]
        current_location_dictionary[self.path_to_save[-1]] = self.pipeline.activate(raw_input)

