from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent

install_requires = [
    line.strip()
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]

setup(
    name="rdf2graph",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=install_requires,
)
