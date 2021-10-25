import threading
import time

class Scheduler():
    """
    This is a class to schedule the polling of the state of the jobs.

    Attributes:
        orchestrator: The orchestrator object that is used to poll the state of the jobs.
        interval: The interval in seconds between each poll.

    """
    def __init__(self, orchestrator, interval):
        self.orchestrator = orchestrator
        self.interval = interval
        
        print("Polling thread created")
        self._running = True
        self.thread = threading.Thread(target=self.polling_loop, args =(lambda : self._running, ), daemon=True)

    def run(self):
        self.thread.start()
        

    def polling_loop(self, _running):
        while self._running:
            self.orchestrator.poll_state()
            time.sleep(self.interval)

    def terminate(self):
        self._running = False