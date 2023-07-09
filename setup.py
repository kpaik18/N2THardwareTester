from setuptools import find_packages, setup

setup(
    name="n2t-hardware-tester",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "PyYAML~=6.0",
        "requests",
        "typer",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    entry_points={
        "console_scripts": [
            "n2t-test=n2t_hardware_tester.main:app",
        ],
    },
    package_data={
        'n2t_hardware_tester': ['cmdi/data/*.yml'],
    },
    include_package_data=True,
)
