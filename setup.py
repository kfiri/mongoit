from setuptools import find_packages, setup


setup(name='mongomedels',
      version='0.0.0',
      author='Kfir Nissim',
      author_email='kfirr99@gmail.com',
      license='MIT',
      description='A pythonic package to work with the interface of pymongo',
      install_requires=['pymongo>=3.5', 'six'],  # TODO until V0.1.0: Validate pymongo version.
      packages=find_packages()
)
