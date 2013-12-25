from distutils.core import setup

setup(
        name='Kinder',
        version='0.1.0',
        author='John J. Wang',
        author_email='john@zinc.io',
        packages=['kinder'],
        scripts=[],
        url='',
        license='LICENSE',
        description='Probabilistic testing framework.',
        long_description=open('README.md').read(),
        install_requires=[
            "unittest >= 1.0.0"
            ],
        )
