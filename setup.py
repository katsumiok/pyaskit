from setuptools import setup, find_packages

setup(
    name="pyaskit",
    version="1.2.1",
    packages=find_packages(),
    description="AskIt: Unified programming interface for programming with large language models (GPT-3.5, GPT-4, Llama 2)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Katsumi Okuda",
    author_email="okuda@csail.mit.edu",
    url="https://github.com/katsumiok/pyaskit",
    python_requires=">=3.7",
    install_requires=[
        "openai",
        "unidecode",
        "timeout-decorator",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    keywords="openai,gpt,gpt-3,gpt-4,llama,api,wrapper,framework,dsl,llm"
)
