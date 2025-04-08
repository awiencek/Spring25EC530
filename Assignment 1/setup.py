from setuptools import setup, find_packages

setup(
    name="geo_distance",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",  # Add pandas if you're using it
        "numpy",   # Add numpy if you're using it
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command-line interface (CLI) commands if applicable
            # For example: "geo-distance = geo_distance:main_function"
        ],
    },
    test_suite="tests",
    tests_require=[
        "pytest",  # Add test dependencies like pytest here
    ],
    author="Your Name",
    author_email="your-email@example.com",
    description="A Python package to calculate geographic distances and find closest locations.",
    long_description=open("README.md").read(),  # Optional: if you have a README.md
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
