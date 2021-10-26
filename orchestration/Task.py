import logging
import datetime

logger = logging.getLogger(__name__)
import threading
import unittest

# rewrite Task so that if the task fails after max retry, a fail over function is called, if provided.
class Task:
    """
    This is a class that defines a task to be run.

    Args:
        function (function): The function to be run.
        *args (list): The arguments to be passed to the function.
        max_retry (int): The maximum number of times to retry running the function
            in case of an exception.
        fail_over_function (function): The function to be run if the task fails after max retry

    Attributes:
        function (function): The function to be run.
        args (list): The arguments to be passed to the function.
        retry_count (int): The number of times the function has been retried.
        max_retry (int): The maximum number of times to retry running the function
            in case of an exception.
        fail_over_function (function): The function to be run if the task fails after max retry

    """
    def __init__(self, function, *args, max_retry=0, fail_over_function=None):
        self.function = function
        self.args = args
        self.retry_count = 0
        self.max_retry = max_retry
        self.fail_over_function = fail_over_function

    def run(self):
        self.start_time = datetime.datetime.now()
        try:
            self.function(*self.args)
        except Exception as e:
            logger.error("Error running task {}".format(self.function.__name__))
            logger.error(e)
            if self.retry_count < self.max_retry:
                self.retry_count += 1
                self.run()
            else:
                if self.fail_over_function is not None:
                    self.fail_over_function()
                raise e
        self.end_time = datetime.datetime.now()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        return self.end_time - self.start_time

# A test of the class Task, with max retry set to 2 where the function provided fails fail the first time it is called.
def test_function():
    if test_function.fail_count == 0:
        test_function.fail_count += 1
        raise Exception("Test exception")
    else:
        print("Success")

def fail_over_function():
    print("Fail over function called")

class TestTask(unittest.TestCase):
    def test_task(self):
        test_function.fail_count = 0
        task = Task(test_function, max_retry=2, fail_over_function=fail_over_function)
        task.run()
        self.assertEqual(task.retry_count, 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
