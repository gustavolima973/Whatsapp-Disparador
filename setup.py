
from setuptools import setup, find_packages
import os

setup(
    name="whatsapp_disparador",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "selenium>=4.0",
        "pandas>=1.3",
        "openpyxl>=3.0",
        "webdriver-manager>=3.0"
    ],
    entry_points={
        "console_scripts": [
            "disparador-whatsapp=whatsapp_disparador.main:main"
        ],
    },
    author="Seu Nome",
    description="Automação de disparos via WhatsApp",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)