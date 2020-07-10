import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-launch-library",
    version="0.6",
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
        "Programming Language :: Python :: 3.6"
    ],
    install_requires=[
        "requests>=2.22,<3",
        "python-dateutil>=2.8,<3",
        "aiohttp>=3.6,<4",
        "unidecode>=1,<2"
    ],
    python_requires='>=3.6'
)
