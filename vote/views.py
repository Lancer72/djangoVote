import random

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from vote.captcha import Captcha
from vote.models import Subject, Teacher, RegisterForm, LoginForm, User


def show_subjects(request):
    subjects=Subject.objects.all()
    return render(request,'subjects.html',{'subjects':subjects})

def show_teachers(request):
    try:
        sno=int(request.GET['sno'])
        subject=Subject.objects.get(no=sno)
        teachers=subject.teacher_set.all()
        return render(request,'teachers.html',{'subject':subject,'teachers':teachers})
    except(KeyError,ValueError,Subject.DoesNotExist):
        return redirect('/')

def praise_or_criticize(request:HttpRequest):
    # 判断用户是否登录
    if 'username' in request.session:
        # 好评
        try:
            tno=int(request.GET['tno'])
            teacher=Teacher.objects.get(no=tno)
            if request.path.startswith('/praise'):
                teacher.good_count+=1
            else:
                teacher.bad_count+=1
            teacher.save()
            data={'code':200,'hint':'操作成功'}
        except(ValueError,Teacher.DoesNotExist):
            data={'code':404,'hint':'操作失败'}
    else:
        data={'code':401,'hint':'请先登录'}
    return JsonResponse(data)

def register(request):
    page,hint='register.html',''
    if request.method=="POST":
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            page='login.html'
            hint='注册成功，请登录'
        else:
            hint='请输入有效的注册信息'
    return render(request,page,{'hint':hint})

# 验证码生成
ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_captcha_text(length=4):
    selected_chars= random.choices(ALL_CHARS,k=length)
    return ''.join(selected_chars)

def get_captcha(request):
    # 获取验证码
    captcha_text=get_captcha_text()
    request.session['captcha']=captcha_text
    image=Captcha.instance().generate(captcha_text)
    return HttpResponse(image,content_type='image/png')

# 处理登录
def login(request):
    hint='请登录'
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            # 验证验证码
            captcha_from_user=form.cleaned_data['captcha']
            captcha_from_sess=request.session.get('captcha','')
            if captcha_from_sess.lower()!=captcha_from_user.lower():
                hint='请输入正确的验证码'
            else:
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=User.objects.filter(username=username,password=password).first()
                if user:
                    # 登录成功后将用户no和用户名保存在session中
                    request.session['userid']=user.no
                    request.session['username']=user.username
                    return redirect('/')
                else:
                    hint='用户名或密码错误'
        else:
            hint='请输入有效的登录信息'
    return render(request,'login.html',{'hint':hint})

def logout(request):
    # 注销
    request.session.flush()
    return redirect('/')