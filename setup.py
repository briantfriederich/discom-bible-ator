from setuptools import setup

setup(name='discombibleator',
      version="1.92",
      packages = ['discombibleator'],
      package_dir = {'discombibleator': 'discombibleator'},
      package_data={'discombibleator': ['data/*.csv']},
      include_package_data=True,
      author = "Brian Friederich",
      author_email = "briantfriederich@gmail.com",
      zip_safe=False)
