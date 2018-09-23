import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-launch-library",
    version="0.2",
    author="Nir Harel",
    author_email="nir@nirharel.space",
    description="A wrapper for the launchlibrary.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Plutoberth/python-launch-library",
    packages=setuptools.find_packages(exclude=".gitignore"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",

    ],
    install_requires=[
        "requests",
        "python-dateutil"
    ]
)