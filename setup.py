import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# python setup.py sdist
# twine upload dist/*

setuptools.setup(
    name="python-launch-library",
    version="2.0.0",
    author="Nir Harel",
    author_email="nir@nirharel.dev",
    description="A wrapper for the launchlibrary.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Plutoberth/python-launch-library",
    packages=setuptools.find_packages(exclude=".gitignore"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=[
        "requests>=2.22,<3",
        "python-dateutil>=2.8,<3",
        "aiohttp>=3.6,<4",
        "unidecode>=1,<2",
        "async_lru>=1.0.2,<2"
    ],
    python_requires='>=3.6'
)
