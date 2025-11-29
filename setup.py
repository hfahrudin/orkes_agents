from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orkes_agents",
    version="0.1.0",
    author="Hasby Fahrudin",
    author_email="fahrudinhasby12@gmail.com",
    description="Agentic based tools with Orkes as backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hfahrudin/orkes_agents",
    packages=find_packages(),
    install_requires=[
        "orkes",
        "duckduckgo_search"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Build Tools",
    ],
    entry_points={
        "console_scripts": [
            "orkes_agents=orkes_agents.cli:main"
        ]
    },
    python_requires=">=3.8",
)
