from setuptools import setup, find_packages

setup(
    name="rhodynamics",
    version="2.1.0",
    description="RhoDynamics: Quantum-inspired Retrieval-Augmented Generation (Q-RAG) Middleware",
    author="RhoDynamics Research Lab",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "requests",
        "qiskit>=1.0.0",
        "qiskit-aer",
        "python-dotenv",
        "rich",
        "matplotlib",
        "seaborn",
        "sqlalchemy",
        "pandas"
    ],
    extras_require={
        "hardware": ["qiskit-ibm-runtime", "pylatexenc"],
        "openai": ["openai"],
        "anthropic": ["anthropic"],
        "benchmarks": ["sentence-transformers"],
        "test": ["pytest", "pytest-cov"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "rhodynamics-cli=rhodynamics.cli:main",
        ]
    },
    python_requires=">=3.8",
)
