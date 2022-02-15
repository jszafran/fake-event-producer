import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fake-event-producer",
    version="0.0.1",
    author="Jakub Szafran",
    author_email="jszafran.pv@gmail.com",
    description="Helper package for generating fake events.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jszafran/fake-event-producer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
