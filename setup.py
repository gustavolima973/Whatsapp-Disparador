
from setuptools import setup, find_packages

setup(
    name="whatsapp_disparador",
    version="1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'selenium>=4.10.0',
        'pandas>=2.0.3',
        'openpyxl>=3.0.0'
    ],
    entry_points={
        'console_scripts': [
            'whatsapp-disparador=main:main',
        ],
    },
)