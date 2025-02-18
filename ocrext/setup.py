from setuptools import setup, find_packages

setup(
    name="ocrext",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytesseract",
        "pillow",
        "opencv-python"
    ],
    description="Python OCR library for scanning dates from images.",
    author="LRCLP",
    license="MIT"
)