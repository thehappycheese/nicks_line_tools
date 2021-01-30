from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Measurements',
    url='https://github.com/thehappycheese/',
    author='Nick',
    # Needed to actually package something
    packages=['nicks_line_tools'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='polyline offset algorithm without dependencies',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)