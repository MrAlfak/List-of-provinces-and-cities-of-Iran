from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iran-cities",
    version="2.0.0",
    author="MrAlfak",
    author_email="",
    description="Complete list of Iranian provinces and cities with geographic coordinates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Persian",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
    ],
    package_data={
        "": ["*.json", "*.csv", "*.sql", "*.geojson"],
    },
    include_package_data=True,
    keywords="iran cities provinces geography coordinates persian farsi",
    project_urls={
        "Bug Reports": "https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues",
        "Source": "https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran",
        "Documentation": "https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/blob/main/docs/API.md",
    },
)
