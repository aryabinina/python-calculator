import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycalc-ariabinina",
    version="0.0.2",
    author="Aleksandra Riabinina",
    author_email="poor-fantazy@yandex.ru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)