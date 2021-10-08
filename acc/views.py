from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages

# Create your views here.


def index(request):
    messages.error(request, "에러발생!!")
    messages.success(request, "회원가입완료")
    messages.warning(request, "경고")
    messages.info(request, "사진바꿔주세요")
    return render(request, "index.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            print(dir(request))
            return redirect("acc:index")
    return render(request, "acc/login.html")


def logout_user(request):
    logout(request)
    return redirect("acc:index")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if User.objects.filter(username=username):
            messages.error(request, "username이 이미 존재합니다.")
            return redirect("acc:signup_user")
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        comment = request.POST.get('comment')
        userpic = request.FILES.get('userpic')
        if not userpic:
            userpic = "none.png"
            messages.info(request, "사진이 기본값으로 설정되었습니다. '정보수정' 에서 사진을 넣어주세요")

        User.objects.create_user(username=username, password=password,
                                 nickname=nickname, comment=comment, userpic=userpic).save()

        return redirect("acc:login_user")
    return render(request, "acc/signup.html")


def profile_user(request):

    return render(request, "acc/profile.html")


def detail(request, num):
    try:
        b = Board.objects.get(id=num)
    except:
        return render(request, "error/notfound.html")


def update(request):
    user = request.user.username
    u = User.objects.get(username=user)
    if request.method == "POST":
        p = request.POST.get("password")
        if p:
            u.set_password(p)
        u.nickname = request.POST.get("nickname")
        u.comment = request.POST.get("comment")
        up = request.FILES.get('userpic')
        if up:
            u.userpic = up
        u.save()
        user_auth = authenticate(username=user, password=p)
        login(request, user_auth)
        return redirect("acc:profile_user")

    return render(request, "acc/update.html")


def delete(request):
    User.objects.get(username=request.user.username).delete()
    return redirect('acc:login_user')


def assign(request):
    if not request.user.userpic:
        u = User.objects.get(username=request.user.username)
        u.userpic = "none.png"
        u.save()
    return redirect("acc:index")
