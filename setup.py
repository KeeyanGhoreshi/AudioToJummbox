import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audioToJummbox",
    version="0.0.1",
    author="Keeyan Ghoreshi",
    author_email="keeyan.ghoreshi@uconn.edu",
    description="Converts audio into jummbox notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeeyanGhoreshi/AudioToJummbox",
    project_urls={
        "Bug Tracker": "https://github.com/KeeyanGhoreshi/AudioToJummbox/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),    
    python_requires=">=3.6",
    entry_points={"console_scripts": ["audioToJummbox = audioToJummbox.main:main"]}
)