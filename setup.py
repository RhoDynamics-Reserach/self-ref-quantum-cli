from setuptools import setup, find_packages

setup(
    name="quantum-rag-layer",
    version="1.0.0",
    description="Quantum-inspired Retrieval-Augmented Generation (RAG) Middleware for Chatbots",
    author="Quantum Synergy Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "requests",
        "qiskit>=1.0.0",
        "qiskit-aer",
        "qiskit-ibm-runtime",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)
