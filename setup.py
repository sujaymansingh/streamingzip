import setuptools

URL = "https://github.com/sujaymansingh/streamingzip"
DESCRIPTION = "View the github page: {0} for more details".format(URL)

if __name__ == "__main__":
    setuptools.setup(
        name="streamingzip",
        version="0.0.1",
        author="Sujay Mansingh",
        author_email="sujay.mansingh@gmail.com",
        packages=setuptools.find_packages(),
        scripts=[],
        url="https://github.com/sujaymansingh/streamingzip",
        license="LICENSE.txt",
        description="A function to gzip an input file.",
        long_description=DESCRIPTION,
    )
