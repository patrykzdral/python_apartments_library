# setup.py
from setuptools import setup, find_packages

setup(name='python_apartments_library',
      version='1.0',
      author='Patryk Zdral',
      author_email='220878@student.pwr.edu.pl',
      description='Library designed for calculating house prices.',
      install_requires=['googlemaps'],
      delete_packages=find_packages(exclude=['tests*', ]),
      url='https://git.e-science.pl/pzdral220878/python_apartments_library',
      packages=['exception', 'library', 'google_addon'],
      )
