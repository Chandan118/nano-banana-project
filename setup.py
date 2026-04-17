"""
Setup configuration for Nano Banana Model.

Author: Chandan Kumar
Email: chandan@bit.edu.cn
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="nano-banana-model",
    version="1.0.0",
    author="Chandan Kumar",
    author_email="chandan@bit.edu.cn",
    description="A lightweight model for banana analysis and classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nano-banana-project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nano-banana=src.nano_banana:main",
        ],
    },
)
