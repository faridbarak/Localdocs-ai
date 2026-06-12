from setuptools import setup, find_packages

setup(
    name="localdocs",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.0.0",
        "typer>=0.12.0",
    ],
    entry_points={
        "console_scripts": [
            "localdocs = localdocs.cli:app",
        ],
    },
)
