from setuptools import find_packages, setup

# TODO until V0.2.0: use sphinx to generate doc.


setup(name='mongomedels',
      version='0.0.1',
      author='Kfir Nissim',
      author_email='kfirr99@gmail.com',
      license='MIT',
      description='A pythonic package to work with the interface of pymongo for the Mongo DB',
      install_requires=['pymongo>=3.5', 'pytz'],  # TODO until V0.1.0: Validate pymongo version.
      packages=find_packages()
)
