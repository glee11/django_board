from django.shortcuts import render
from googletrans import Translator


def index(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get('before')
        if text:
            f = request.POST.get('from')
            t = request.POST.get('to')
            translator = Translator()
            print(text)
            if f == 'dt':
                trans = translator.translate(text, dest=t)
            elif not f:
                trans = translator.translate(text, dest='ko')
            else:
                trans = translator.translate(text, src=f, dest=t)

            context.update({
                'after': trans.text,
                'before': text,
                'from': f,
                'to': t,
            })

    return render(request, "trans/index.html", context)
