from django.shortcuts import render
from PIL import Image
import pytesseract
import pdfplumber


def index(request):
    pytesseract.pytesseract.tesseract_cmd = 'tess/tesseract.exe'
    context = {}
    if request.method == "POST":
        file = request.FILES.get('tesbefore')
        print("sibal")
        if file:
            t = file.content_type.split('/')
        else:
            return render(request, "error/notfound.html")
        print(t[1])
        if t[0] == "image":
            im = Image.open(file)
            f = request.POST.get('from')
            text = pytesseract.image_to_string(im, lang=f)
            context.update({
                'after': text,
                'f': f,
            })
        elif t[0] == "application" and t[1]=="pdf":
            text = ''
            with pdfplumber.open(file) as pdf:
                for i in range(len(pdf.pages)):
                    first_page = pdf.pages[i]
                    print(first_page.extract_text())
                    text += first_page.extract_text()
                    print(i+1)

            context.update({
                'after': text,
            })
        else:
            return render(request, "error/notfound.html")
    return render(request, "ocr/index.html", context)


"""with pdfplumber.open("dddd.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.extract_text())"""
