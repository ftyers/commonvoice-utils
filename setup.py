import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="commonvoice-utils",
    version="0.1.4",
    description="Linguistic processing for languages in Common Voice",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ftyers/commonvoice-utils",
    author="Francis M. Tyers",
    author_email="ftyers@prompsit.com",
    license="AGPL",
    classifiers=[
	"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    packages=['cvutils']
)

