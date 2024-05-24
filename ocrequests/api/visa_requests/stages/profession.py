from ocrequests.api.visa_requests.stages.stage import Stage
from datetime import datetime, timedelta

YEAR = 365


class DetermineProfessionStage(Stage):
    def run(self, stage_input: datetime):
        underage = datetime.now() - stage_input <= timedelta(days=YEAR) * 18
        return {
            "id": 123 if underage else 55,
            "code": "PR31" if underage else "PR14",
            "libelle": "WITHOUT" if underage else "EMPLOYEE",
            "lang": "en",
            "statut": "Active",
            "active": True,
        }
