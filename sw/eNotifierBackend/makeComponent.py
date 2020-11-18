from setuptools import sandbox


sandbox.run_setup('setup.py', ['clean', 'bdist_wheel'])