#Web appliction for  Extracting Business Card Details using Easy OCR.
This repository contains code to extract business card details using EasyOCR, a Python package for OCR (Optical Character Recognition) that supports over 70 languages and has pretrained models for a variety of use cases.

# Getting Started
To get started with using EasyOCR, you will need to install the package. You can do this by running the following command:

# Copy code
## pip install easyocr

Once you have installed EasyOCR, you can use the code in this repository to extract details from business cards.

# Usage
The code in this repository contains a Python script main.py that demonstrates how to use EasyOCR to extract details from a business card. The script takes an image file path as input and outputs the extracted details as a dictionary.  Then this data is used for GUI building which offers following featues.

Simple streamlit GUI which offers:
1) Data extraction
2) Save data to database using sqlite3
3) View data
4) Delete data ,using emain authentication

To use the script, simply run the following command, replacing image_path with the path to the image file you want to extract details from:


The output will be a dictionary containing the following fields:

### name: The name of the person on the business card.
### email: The email address on the business card.
### phone: The phone number on the business card.
### company: The name of the company on the business card.
### Address: The address of the person on the business card.



# Contributing

If you would like to contribute to this repository, please feel free to submit a pull request. We welcome contributions from the community.
