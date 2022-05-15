from datetime import datetime
import enum


class TimeSimulation:
    def __init__(self, resolution, start, end, last_point) -> None:
        # TODO refactor with more options.
        self.resolution = Resolution(resolution)
        self.start = int(datetime.strptime(
            start, "%Y-%m-%d %H:%M:%S").timestamp()*1000)
        self.end = int(datetime.strptime(
            end, "%Y-%m-%d %H:%M:%S").timestamp()*1000)
        self.current_time = self.start
        self.stop_reason = None
        self.last_point = last_point

    def update_current_timestamp(self):
        self.current_time += self.resolution.step
        return self.current_time

    def stop(self) -> bool:
        if self.current_time >= self.last_point:
            self.stop_reason = 'last_point'
            return True
        if self.current_time > self.end:
            self.stop_reason = 'end'
            return True

        return False


class Resolution:
    day = 24*60*60*1000
    hour = 60*60*1000
    minute = 60*1000

    def __init__(self, resolution):
        if resolution == 'day':
            self.step = self.day
        elif resolution == '1h':
            self.step = self.hour
        elif resolution == '1min':
            self.step = self.minute
        else:
            raise ValueError('Invalid resolution')
