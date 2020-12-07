from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='threatscrape',
    version='0.0.1',
    description='Scrape Threat Information from different sources',
    long_description=readme,
    author='Threat Lead',
    author_email='threatlead@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'samples')),
    install_requires=[
        'scrapy',
        'dateparser',
    ]
)
