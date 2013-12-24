import random
import unittest
import test_job

class MainGenerator:
    def __init__(self, test_jobs, param_generators, options = None):
        self.test_jobs = MarkovProcess(test_jobs)
        self.param_generators = {key: MarkovProcess(gens) for key, gens in param_generators.iteritems()}
        self.unit_test_runner = UnitTestRunner()
        self.options = options

        self._enforce_invariants(self.test_jobs, self.param_generators)

    def run(self):
        pass

    def step(self):
        test = self.test_jobs.generate()
        params = self.param_generators[test].generate()
        self.unit_test_runner.run_tests(test, params)

    def _enforce_invariants(self, test_jobs, param_generators):
        if len(param_generators) != len(test_jobs.prob_hash):
            raise "test_jobs and param_generators inputs must match"
        for key in test_jobs.prob_hash.iterkeys():
            if not isinstance(key, test_job.TestJob):
                raise "Must subclass TestJob class for all tests"
            if key not in param_generators:
                raise "test_jobs and param_generators inputs must match"

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
            raise "Inputs to a MarkovProcess must be either an array or a dictionary"

    def generate(self):
        rand = random.random()
        total = 0
        for key, prob in self.prob_hash.iteritems():
            total += prob
            if rand <= total:
                return key
