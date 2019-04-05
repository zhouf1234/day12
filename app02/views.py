from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

#检查用户是否登录的装饰器
def wrapper(func):
    def inner(request,*args,**kwargs):
        #登录校验
        cookie_k=request.get_signed_cookie('k',None,salt='s1')
        if cookie_k:
            # 表示已经登录的用户就前往这个页面
            ret=func(*args,**kwargs)
            return ret
        else:
            return redirect('/login/')
    return inner


def login(request):
    #上传数据
    if request.method=='POST':
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')
        #校验用户名和密码是否正确
        if user=='alex'and pwd=='123456':
            #登录成功的情况,此次加了cookie,即登录成功后，浏览器自动记住了这个user=alex，下次登录的时候，user默认选项有alex
            rep=redirect('/index/')
            # 此条加的cookie过于简单，不安全
            # rep.set_cookie('user',user)

            #设置超时时间的另一个方法，了解就行
            # import datetime
            # now=datetime.datetime.now()
            # d=datetime.timedelta(seconds=10)
            #rep.set_signed_cookie('user2', user, salt='s1', expires=now+d)


            #此条加的cookie进行了加密处理，salt=‘s1’，这个s1随意写的
            #max_age=10:设置cookie的时效性为10秒，期间不用重新登录，如果不写，会一直是登录的状态
            #path='/index/',指定做的所有操作只有index看到，与其他的毫无关系
            rep.set_signed_cookie('k',user,salt='s1',max_age=100,path='/index/')
            return rep
    return render(request,'login.html')


def index(request):
    # 获取到cooki里的user的信息，此条对应的是上方的rep.set_cookie('user',user)
    # user=request.COOKIES.get('user')
    #user = request.get_signed_cookie('user2',salt='s1')也可以，user2这个键可以随意写的，和设置的 rep.set_signed_cookie('user2',user,salt='s1')一致
    cookie_k=request.get_signed_cookie('k',None,salt='s1')
    if cookie_k:
        #表示已经登录的用户
        return render(request, 'index.html')
    else:
        #再去登录
        return redirect('/login/')

@wrapper
def home(request):
    return render(request,'home.html')



