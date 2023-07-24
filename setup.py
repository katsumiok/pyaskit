from setuptools import setup, find_packages

setup(
    name="pyaskit",
    version="1.0.0",
    packages=find_packages(),
    description="AskIt: Language support for programming with large language models (GPT-3.5, GPT-4).",
    author="Katsumi Okuda",
    author_email="okuda@csail.mit.edu",
    url="https://github.com/katsumiok/pyaskit",
    python_requires=">=3.7",
    install_requires=[
        "openai",
        "unidecode",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
)
