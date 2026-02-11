"""
Setup configuration for P³ Framework
ACL 2026 Anonymous Submission
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="p3-framework",
    version="0.1.0",
    description="Dynamic Persona Coherence via Hierarchical Psychological State Modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anonymous",
    author_email="anonymous@example.com",
    url="https://anonymous.4open.science/",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="persona coherence, role-playing agents, LLM, psychological modeling, NLP",
)
