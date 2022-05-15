from datetime import datetime


class TimeSimulation:
    def __init__(self, resolution, start, end, last_point) -> None:
        # TODO refactor
        if resolution == 'day':
            self.step = 24*60*60
        elif resolution == '1h':
            self.step = 60*60
        elif resolution == '1min':
            self.step = 60
        else:
            raise ValueError('Invalid resolution')
        self.start = datetime.strptime(
            start, "%Y-%m-%d %H:%M:%S").timestamp()
        self.end = datetime.strptime(
            end, "%Y-%m-%d %H:%M:%S").timestamp()
        self.current_time = self.start
        self.stop_reason = None
        self.last_point = last_point

    def update_current_timestamp(self):
        self.current_time += self.step
        return self.current_time

    def stop(self) -> bool:
        if self.current_time >= self.last_point:
            self.stop_reason = 'last_point'
            return True
        if self.current_time > self.end:
            self.stop_reason = 'end'
            return True

        return False
