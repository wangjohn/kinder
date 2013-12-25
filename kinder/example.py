import main_generator
import test_job
import param_generator

class ExampleJob(test_job.TestJob):
    def test_me(self):
        print 'testing %s' % self.params

class ExampleGenerator(param_generator.ParamGenerator):
    def generate_params(self):
        return "generating params"

if __name__ == '__main__':
    test_jobs = {
            ExampleJob: 1
            }

    param_generators = {
            ExampleJob: {
                ExampleGenerator(): 1
                }
            }

    runner = main_generator.UnitTestRunner()
    main_generator.MainGenerator(test_jobs, param_generators).run()
