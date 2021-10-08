import pdfplumber
import sys

print(sys.argv[1])
print(sys.argv[2])


with pdfplumber.open("dddd.pdf") as pdf:
    first_page = pdf.pages[0]

    print(first_page.extract_text())
