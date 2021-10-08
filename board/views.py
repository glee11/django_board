from django.shortcuts import render, redirect
from . models import Board, Reply
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.


def index(request):
    if not request.user.username:
        return redirect("acc:login_user")
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    cate = request.GET.get('cate', '')

    if kw:
        if cate == 'subject':
            b = Board.objects.filter(subject__contains=kw).order_by("-c_time")
        elif cate == 'writer':
            b = Board.objects.filter(writer__contains=kw).order_by("-c_time")
        elif cate == 'content':
            b = Board.objects.filter(content__contains=kw).order_by("-c_time")
    else:
        b = Board.objects.order_by("-c_time")
    pag = Paginator(b, 10)
    obj = pag.get_page(page)
    context = {
        'con': obj,
        'kw': kw,
        'cate': cate,
    }
    return render(request, "board/index.html", context)


def detail(request, num):
    if not request.user.username:
        return redirect("acc:login_user")

    try:
        b = Board.objects.get(id=num)
        r = b.reply_set.all()
        context = {
            'con': b,
            'rep': r,
        }
    except:
        return render(request, "error/notfound.html")

    return render(request, "board/detail.html", context)


def create(request):
    if not request.user.username:
        return redirect("acc:login_user")
    if request.method == "POST":
        subject = request.POST.get("subject")
        writer = request.user.username
        content = request.POST.get("content")
        Board(subject=subject, writer=writer, content=content,
              likey=0, c_time=timezone.now()).save()
        return redirect("board:index")

    return render(request, "board/create.html")


def delete(request, conid):
    if not request.user.username:
        return redirect("acc:login_user")

    try:
        b = Board.objects.get(id=conid)
        if b.writer == request.user.username:
            b.delete()
        else:
            return render(request, "error/forbidden.html")
    except:
        return render(request, "error/forbidden.html")
    return redirect("board:index")


def update(request, conid):
    if not request.user.username:
        return redirect("acc:login_user")

    b = Board.objects.get(id=conid)
    if request.user.username == b.writer:
        if request.method == "POST":
            b.subject = request.POST.get("subject")
            b.content = request.POST.get("content")
            b.save()
            return redirect("board:detail", num=conid)
        context = {
            'con': b
        }
        return render(request, "board/update.html", context)
    else:
        return render(request, "error/forbidden.html")


def create_reply(request, conid):
    if not request.user.username:
        return redirect("acc:login_user")

    b = Board.objects.get(id=conid)
    r = request.user.username
    c = request.POST.get('comment')
    p = request.user.userpic
    Reply(subject=b, replyer=r, comment=c, pic=p).save()
    return redirect("board:detail", num=conid)


def delete_reply(request, conid, num):
    if not request.user.username:
        return redirect("acc:login_user")

    r = Reply.objects.get(id=num).delete()
    if request.user.username == r.replyer:
        r.delete()
    else:
        messages.error(request, "잘못된 접근입니다.")
        return render(request, "error/forbidden.html")
    return redirect("board:detail", num=conid)


def up(reqeust, conid):
    b = Board.objects.get(id=conid)
    if reqeust.user in b.up.all():
        return redirect("board:detail", num=conid)
    b.up.add(reqeust.user)

    return redirect("board:detail", num=conid)


def cancel(reqeust, conid):
    b = Board.objects.get(id=conid)
    if reqeust.user in b.up.all():
        b.up.remove(reqeust.user)

    return redirect("board:detail", num=conid)
