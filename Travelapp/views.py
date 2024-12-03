from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Travelapp.models import package,Cart,ConfirmBooking
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def index(request): 
    carousel_images = package.objects.filter(is_active=True)[:5]  # Fetch top 5 packages for the carousel
    context={}
    p=package.objects.filter(is_active=True)
    context['packages']=p
    context['carousel_images'] = carousel_images
    print(p)
    return render(request,'index.html',context)


def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=package.objects.filter(q1 & q2)
    print(p)
    context={}
    context['packages']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=package.objects.filter(q1 & q2 & q3)
    context={}
    context['packages']=p
    return render(request,'index.html',context) 


def sort(request,sv):
    if sv=='1':
        col='price'
    else:
        col='-price'
    p=package.objects.filter(is_active=True).order_by(col)
    context={}
    context['packages']=p
    return render(request,'index.html',context)  


def pdetails(request,pid):
    p=package.objects.filter(id=pid)
    context={}
    context['packages']=p
    return render(request,'packages.html',context)


def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password not matching"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['successmsg']="User Registered Successfully!!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User Already Exists, use another emailID"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,upass)
        context={}
        if uname=="" or upass=="" :
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="Invalid Username or Password!"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def ulogout(request):
    logout(request)
    return redirect('/index')

def About(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def viewbook(request):
    if not request.user.is_authenticated:
        return redirect('/ulogin')
    c=Cart.objects.filter(uid=request.user.id)
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    print(s)
    np=len(c)
    context={}
    context['data']=c
    context['total']=s
    context['items']=np
    context['user_email']=request.user.email
    return render(request,'viewbook.html',context)


def addtobook(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=package.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(len(c))
        context={}
        context['packages']=p
        n=len(c)
        if n==1:
            context['errmsg']="Package already exists in the Bookings!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context["success"]="Package Added to Bookings!"
        return render(request,'packages.html',context)
    else:
        return redirect("/ulogin")

def makepayment(request):
    orders=ConfirmBooking.objects.filter(uid=request.user.id)
    np=len(orders)
    s=0
    for  x in orders:
        s=s+x.pid.price*x.qty
        B_id=x.B_id
    client = razorpay.Client(auth=("rzp_test_wIRW5UcLnuojt3", "TAWQaJo7pF8PxWMwC5MwnOQg"))

    data = { "amount": s*100, "currency": "INR", "receipt": B_id }
    payment = client.order.create(data=data)
    print(payment)
    return render(request,'pay.html')


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewbook')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)

    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewbook")

def confirmbooking(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    B_id=random.randrange(1000,9999)
    for x in c:
        o=ConfirmBooking.objects.create(B_id=B_id,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=ConfirmBooking.objects.filter(uid=userid)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['items']=np
    return render(request,'confirmbooking.html',context)

def search(request):
    query = request.GET.get('q')
    if query:
        packages = package.objects.filter(name=query)
    else:
        packages = package.objects.all()
    return render(request, 'index.html', {'packages': packages, 'search_query': query})
    #return render(request, 'index.html', {'packages': package})

def senduseremail(request):
    try:
        send_mail(
        "Subject here",
        "Here is the message.",
        "shravanikhandagale0382@gmail.com",
        ["shravanikhandagale2104@gmail.com"],
        fail_silently=False,
        )
        return HttpResponse("Mail sent Successfully!! ")
    except Exception:
        return HttpResponse("Mail sent Successfully!! ")