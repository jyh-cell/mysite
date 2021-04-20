from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib   # 此模块用于给密码加密
# 导入了redirect，用于logout后，页面重定向到‘/login/’这个url


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, '../templates/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, '../templates/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, '../templates/login.html', locals())

        else:
            return render(request, '../templates/login.html', locals())

    login_form = forms.UserForm()
    return render(request, '../templates/login.html', locals())


'''
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
                # models.User.objects.get(
                # name=username)是Django提供的最常用的数据查询API
            except :
                message = '用户名不存在！'
                # 注意这里没有区分异常的类型，因为在数据库访问过程中，可能发生很多种类型的异常，我们要对用户屏蔽这些信息，不可以暴露给用户，而是统一返回一个错误提示，比如用户名不存在。这是大多数情况下的通用做法。当然，如果你非要细分，也不是不行。
                return render(request, '../templates/login.html', {'message': message})
            if user.password == password:
                print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, '../templates/login.html', {'message': message})
        else:
            return render(request, '../templates/login.html', {'message': message})
    return render(request, '../templates/login.html')
'''


def register(request):
    '''
从大体逻辑上，也是先实例化一个RegisterForm的对象，然后使用is_valide()验证数据，再从cleaned_data中获取数据。

重点在于注册逻辑，首先两次输入的密码必须相同，其次不能存在相同用户名和邮箱，最后如果条件都满足，利用ORM的API，创建一个用户实例，然后保存到数据库内。

对于注册的逻辑，不同的生产环境有不同的要求，请跟进实际情况自行完善，这里只是一个基本的注册过程，不能生搬照抄。

    '''
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, '../templates/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, '../templates/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, '../templates/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, '../templates/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, '../templates/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
# flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def hash_code(s, salt='mysite'):# 加点盐
    # 使用了sha256算法，加了点盐。
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()




