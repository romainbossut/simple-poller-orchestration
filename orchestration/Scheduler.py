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


if __name__ == '__main__':

#unit tests of this class
    import unittest
    from unittest.mock import Mock

    class TestScheduler(unittest.TestCase):
        def test_run(self):
            orchestrator = Mock()
            scheduler = Scheduler(orchestrator, 1)
            scheduler.run()
            self.assertTrue(scheduler.thread.is_alive())

        def test_terminate(self):
            orchestrator = Mock()
            scheduler = Scheduler(orchestrator, 1)
            scheduler.terminate()
            self.assertFalse(scheduler.thread.is_alive())

    unittest.main()


































































