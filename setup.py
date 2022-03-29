from setuptools import find_packages, setup

requirements = [
    "opensearch-py==1.1.0"
]

setup(
    name="elasticlogger",
    version="0.0.0",
    packages=find_packages(),
    py_modules=["common-elasticsearch"],
    install_requires=requirements,
    include_package_data=True,
)
