class ProximityChecker:
    def __init__(self, actual_string: str, threshold: int):
        self.score = 0
        self.actual_string = actual_string
        self.length_needed = len(actual_string) - threshold

    def update_score(self, score):
        self.score = max(self.score, score)

    def recursive_match(self, actual_string: str, scanned_string: str, score=0):
        # Stopping criteria, possible paths won't reach desired score
        if score + min(len(actual_string), len(scanned_string)) < self.length_needed:
            return
        # Reached the edge, no possible matching remaining
        if len(actual_string) == 0 or len(scanned_string) == 0:
            self.update_score(score)
        # Both continue, found a matched character, therefore score is increased
        elif actual_string[0] == scanned_string[0]:
            self.recursive_match(actual_string[1:], scanned_string[1:], score + 1)
        # Didn't find a matched character, therefore algorithm should split into two remaining possible paths
        else:
            self.recursive_match(actual_string[1:], scanned_string, score),
            self.recursive_match(actual_string, scanned_string[1:], score)

    def is_match(self):
        return self.length_needed <= self.score

    def restart(self):
        self.score = 0

    # Threshold indicates the maximum amount of mismatches allowed between the strings
    def run(self, scanned_string: str) -> int:
        self.restart()
        self.recursive_match(self.actual_string, scanned_string)
        return self.is_match()
