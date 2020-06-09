from setuptools import setup, find_packages

setup(
    name="smart-home",  # Replace with your own username
    version="0.0.1",
    author="Jesus Bernal",
    author_email="j.bernal@upm.es",
    description="Smart Home",
    packages=find_packages(),
    classifiers=[  # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning"
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["raspberry-pi", "smart-home"],
    python_requires='>=3.6',
)
