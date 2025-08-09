from setuptools import setup, find_packages

setup(
    name="ingredient-list-maker",
    version="1.0.0",
    description="Recipe ingredient list maker for shopping",
    author="SakuraiTohya",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["streamlit", "gspread", "google-auth", "beautifulsoup4", "requests"],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "isort>=5.10.0",
            "types-requests",
            "types-beautifulsoup4",
        ]
    },
)
