import kinder
print dir(kinder)

class ExampleJob(kinder.TestJob):
    def test_me(self):
        print 'testing %s' % self.params

class ExampleGenerator(kinder.ParamGenerator):
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

    kinder.MainGenerator(test_jobs, param_generators).run()
