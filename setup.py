from setuptools import setup, find_packages

setup(
    name="fridaDownloader",
    version="1.3.0",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "fridaDownloader=fridaDownloader:main",
        ],
    },
    description="fridaDownloader is a command-line tool that streamlines downloading the Frida Gadget or Server for Android, enabling developers and security researchers to quickly access the components needed for dynamic instrumentation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mateofumis/fridaDownloader",
    author="Mateo Fumis",
    author_email="mateofumis1@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
