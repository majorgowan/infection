import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

this_directory = os.path.abspath(os.path.dirname(__file__))

# read the contents of requirements.txt
with open(os.path.join(this_directory, 'requirements.txt'),
          encoding='utf-8') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="infection",
    version="1.0",
    author="Mark Fruman",
    author_email="majorgowan@yahoo.com",
    description="Package for simulating an epidemic infection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["infection=infection.__main__:main"], },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
