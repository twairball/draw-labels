import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="draw_labels",
    version="0.0.1",
    author="Jerry Liu",
    author_email="twairball@yahoo.com",
    description="Draw graphical labels on images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twairball/draw-labels",
    packages=setuptools.find_packages(),
    install_requires=['numpy'], 
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)