from setuptools import setup, find_packages

setup(
    name="nimble-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.3",
        "scikit-learn>=0.24.2",
        "numpy>=1.21.2",
        "joblib>=1.0.1",
    ],
    extras_require={
        'docs': [
            "sphinx>=4.2.0",
            "sphinx-rtd-theme>=0.5.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "nimble-search=nimble_search.cli:main",
        ],
    },
    # Other metadata
    author="Ahmed Elfarra",
    author_email="elfarradev@gmail.com",
    description="A lightweight, flexible search index for small to medium-sized datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aelfarra/nimble-search",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
