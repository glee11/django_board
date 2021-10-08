from django.shortcuts import render, redirect
from .models import Topic, Choice
from django.utils import timezone
from django.core.paginator import Paginator


def index(request):
    page = request.GET.get("page", 1)
    t = Topic.objects.order_by("-c_time")
    pag = Paginator(t, 2)
    obj = pag.get_page(page)
    context = {
        "con": obj
    }
    return render(request, "vote/index.html", context)


def detail(request, num):
    t = Topic.objects.get(id=num)
    c = t.choice_set.all()
    context = {
        "con": t,
        "cho": c,
    }
    return render(request, "vote/detail.html", context)


def vote(request, conid):
    t = Topic.objects.get(id=conid)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cid = request.POST.get("choice")
        c = Choice.objects.get(id=cid)
        c.cuser.add(request.user)

    return redirect("vote:detail", num=conid)


def cancel(request, conid):
    t = Topic.objects.get(id=conid)
    if request.user in t.voter.all():
        t.voter.remove(request.user)
        c = t.choice_set.all()
        for i in c:
            if request.user in i.cuser.all():
                i.cuser.remove(request.user)
    return redirect("vote:detail", num=conid)


def create(request):

    if request.method == "POST":
        s = request.POST.get("subject")
        w = request.user.username
        c = request.POST.get("comment")
        w_p = request.user.userpic
        if s and c:
            t = Topic(subject=s, writer=w, comment=c,
                      writer_pic=w_p, c_time=timezone.now())
            t.save()
            name = request.POST.getlist('name')
            pic = request.FILES.getlist('pic')
            for i, j in zip(name, pic):
                Choice(subject=t, name=i, pic=j).save()
        return redirect("vote:index")

    return render(request, "vote/create.html")
