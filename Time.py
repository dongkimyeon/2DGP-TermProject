import time


class Time:
    _delta_time = 0.0
    _current_time = time.time()

    @classmethod
    def update(cls):
        now = time.time()
        cls._delta_time = now - cls._current_time
        cls._current_time = now


    @classmethod
    def DeltaTime(cls):
        return cls._delta_time
