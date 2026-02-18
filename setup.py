"""Configuration d'installation pour AGENT_SECRET_ADL."""

from setuptools import setup, find_packages

setup(
    name="agent-secret-adl",
    version="0.1.0",
    description="Extraction et enrichissement de candidatures TAXIS/VTC depuis PDF",
    author="AGENT_SECRET_ADL",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.10.0",
        "pandas>=2.0.0",
        "typer>=0.9.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "agent-secret-adl=agent_secret_adl.__main__:app",
        ],
    },
)
