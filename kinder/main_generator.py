import random
import unittest
import test_job
import multiprocessing

class MainGenerator:
    def __init__(self, test_jobs, param_generators, num_prcoesses = 5):
        self.test_jobs = MarkovProcess(test_jobs)
        self.param_generators = {key: MarkovProcess(gens) for key, gens in param_generators.iteritems()}
        self.unit_test_runners = []
        self.num_processes = 5

        self._enforce_invariants(self.test_jobs, self.param_generators)

    def run(self, num_jobs = 1000):
        queue = multiprocessing.Queue()
        for i in xrange(num_jobs):
            queue.put(self.step())

        for i in xrange(self.num_processes):
            runner = UnitTestRunner()
            self.unit_test_runners.append(runner)
            QueueRunner(queue, runner).start()
        results = [runner.result for runner in self.unit_test_runners]
        return results

    def step(self):
        test = self.test_jobs.generate()
        params = self.param_generators[test].generate().generate_params()
        return (test, params)

    def _enforce_invariants(self, test_jobs, param_generators):
        if len(param_generators) != len(test_jobs.prob_hash):
            raise AssertionError("test_jobs and param_generators inputs must match")
        for key in test_jobs.prob_hash.iterkeys():
            if not issubclass(key, test_job.TestJob):
                raise AssertionError("Must subclass TestJob class for all tests")
            if key not in param_generators:
                raise AssertionError("test_jobs and param_generators inputs must match")

class QueueRunner(multiprocessing.Process):
    def __init__(self, queue, unit_test_runner):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.unit_test_runner = unit_test_runner

    def run(self):
        for item in iter(self.queue.get, "STOP"):
            test, params = item[0], item[1]
            self.unit_test_runner.run_tests(test, params)

class UnitTestRunner:
    def __init__(self, result = None):
        self.result = result if result else unittest.TestResult()
        self.loader = unittest.TestLoader()

    def run_tests(self, klass, params):
        tests = self.loader.getTestCaseNames(klass)
        for test_name in tests:
            klass(params, test_name).run(self.result)

class MarkovProcess:
    def __init__(self, prob_hash):
        self.prob_hash = self._compute_probabilities(prob_hash)

    def _compute_probabilities(self, prob_hash):
        if isinstance(prob_hash, dict):
            total = sum([weight for weight in prob_hash.itervalues()])
            return {key: float(weight) / total for key, weight in prob_hash.iteritems()}
        elif isinstance(prob_hash, list):
            return {key: 1.0 / len(prob_hash) for item in prob_hash}
        else:
            raise AssertionError("Inputs to a MarkovProcess must be either an array or a dictionary")

    def generate(self):
        rand = random.random()
        total = 0
        for key, prob in self.prob_hash.iteritems():
            total += prob
            if rand <= total:
                return key
