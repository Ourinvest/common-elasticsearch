from setuptools import find_packages, setup

requirements = ["opensearch-py==1.1.0"]

setup(
    name="elasticlogger",
    url='https://github.com/Ourinvest/common-elasticsearch.git',
    version="0.0.0",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
