from setuptools import setup, find_packages
# -*- coding: utf-8 -*-

try:
  long_description = open("README.rst").read()
except IOError:
  long_description = ""

setup(
  name="mysite",
  version="0.0.1",
  description="A pip package",
  license="MIT",
  author="manyu",
  packages=find_packages(
      include=['mysite', 'mysite.*']),
  install_requires=[
      "django",
      "autopep8"
  ],
  long_description=long_description,
  classifiers=[
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.8",
  ]
)
