from setuptools import setup, find_packages

setup(
    name="quantum-rg-layer",
    version="1.0.0",
    description="Quantum-inspired Retrieval-Augmented Generation (RAG) Middleware for Chatbots",
    author="Quantum Synergy Team",
    packages=["quantum_rag_layer"],
    package_dir={"quantum_rag_layer": "."},
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)
