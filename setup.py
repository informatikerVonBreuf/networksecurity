"""Package metadata; runtime dependencies are listed in requirements.txt."""
from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="networksecurity",
    version="0.1.0",
    description="Reproducible phishing classification and MLOps demonstration",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=Path("requirements.txt").read_text().splitlines(),
)
