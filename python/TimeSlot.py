class TimeSlot:
    def __init__(self, days=None, start_time=None, end_time=None):
        self.days = days
        self.start_time = start_time
        self.end_time = end_time

    def overlaps(self, other):
        if other is None or self.days is None or other.days is None:
            return False
        if not self.share_days(self.days, other.days):
            return False
        # Convert times to minutes
        this_start = self.to_minutes(self.start_time)
        this_end = self.to_minutes(self.end_time)
        other_start = self.to_minutes(other.start_time)
        other_end = self.to_minutes(other.end_time)

        if this_start < 0 or this_end < 0 or other_start < 0 or other_end < 0:
            return False
        return this_start < other_end and other_start < this_end

    def share_days(self, d1, d2):
        a = d1.upper()
        b = d2.upper()
        tokens = ["TH", "M", "T", "W", "F", "S", "U"]
        for token in tokens:
            if token in a and token in b:
                return True
        return False

    def to_minutes(self, time_str):
        if time_str is None or ":" not in time_str:
            return -1
        try:
            parts = time_str.split(":")
            return int(parts[0]) * 60 + int(parts[1])
        except ValueError:
            return -1

    def __str__(self):
        return f"{self.days} {self.start_time}-{self.end_time}"