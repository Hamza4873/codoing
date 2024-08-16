from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',
        'ipwhois>=1.0.0',
        'shodan>=1.24.0',
        'passivetotal>=1.0.0',
        'pyyaml>=5.4',
        'vt-py>=0.6.0',
        'domaintools_api>=1.0.0',
    ],
    dependency_links=[
        'https://<some_url>/simple/<package_name>'  # Custom index for a specific package
    ],
    python_requires='>=3.6',
)