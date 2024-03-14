from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def about(request):
    return render(request,'about.html')
    #return HttpResponse("Hello from views.py file")
    #x='Hello from views.py file'
    #return HttpResponse(x)


def contact(request):
    return render(request,'contact.html')



def delete(request,rid):
    return HttpResponse("Id to be deleted"+rid)


def edit(request,name):
    return HttpResponse("name to be edited :"+name)
  

class ContactForm(View):
    def get(self,request):
        return HttpResponse("Class based view..!!!")



class Parameter(View):
    def get(self,request,cid):
        return HttpResponse("class based view :"+cid)

def hello(request):
    context={}
    context['x']=100
    context['y']=15
    context['z']=200
    context['l']=[10,20,30,40]
    context['product']=[{'id':1,'image':'pimage','pname':'samsung','pcat':'mobile','price':25000},
    {'id':2,'image':'qimage','pname':'jeans','pcat':'cloth','price':2000}]
    return render(request,'hello.html',context)


def message(request):
    return render(request,'message.html')


def base(request):
    return render(request,'base.html')


def products(request):
    uid=request.user.id
    #print("Loggedin User",uid)
    p=Product.objects.filter(is_active=True)
    #print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

'''
def register(request):
    return render(request,'register.html')
'''

def register(request):
    context={}
    if request.method=="GET":
        return render(request,'register.html')

    else:
        n= request.POST['uname']
        p= request.POST['upass']
        cp= request.POST['ucpass']
        
        
        print(n)
        print(p)
        print(cp)
        
        if n=='' or p=='' or cp=='':
            context['errmsg']="Fields cannot be blank"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Didn't Match!!!!"
            return render(request,'register.html',context)
        elif len(p)<8 or len(p)>15:
            context['errmsg']="Password must be minimum 8 characters and maximum 15 characters"
            return render(request,'register.html',context)
    
        else:
            try:
                 u=User.objects.create(username=n)
                 u.set_password(p)
                 u.save()
                 context['success']="User Created Successfullyy..!!!"
                 return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User Already Exist ,Please Login!!!"
                return render(request,'register.html',context)








'''
def login(request):
    return render(request,'login.html')

'''









def user_login(request):
    if request.method=='GET':
        return render(request,'loginpage.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        
        #print(n)
        #print(p)
        
        u=authenticate(username=n,password=p)
        #print(u)
        if u is not None:
            login(request,u)
            return redirect('/products')

        else:
            context={}
            context['errmsg']='Invalid Username and Password!!'
            return render(request,'loginpage.html',context)
            
'''
def user_login(request):
    return render(request,'login.html')
'''

def user_logout(request):
    logout(request)
    return redirect('/loggedin')



def catfilter(request,cv):
    #print(cv)
    q1=Q(cat=cv)
    q2=Q(is_active=True)


    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)



def sort(request,sv):
    #print("datatype of sv is:",type(sv))
    if sv == '1':
        p=Product.objects.order_by('-price').filter(is_active=True)

    else:
        p=Product.objects.order_by('price').filter(is_active=True)

    context={}
    context['data']=p
    return render(request,'index.html',context)


def filterbyprice(request):
    min=request.GET['min']
    max=request.GET['max']

    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)


def product_detail(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'product_details.html',context)




def cart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        #uid=request.user.id
        #print(u[0])
        #print(uid)
        p = Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context = {}
        context['data']=p
        if n==1:
            context['msg']='Product already exist in cart'
        else:
            c=Cart.objects.create(userid=u[0],pid=p[0])
            c.save
            context['msg']="products added successfully"
            #return HttpResponse("Product adds in cart")
        return render(request,'product_details.html',context)

    else:
        return redirect('/loggedin')
    




def viewcart(request):
    c=Cart.objects.filter(userid=request.user.id)
    sum=0
    for x in c:
        sum = sum + x.pid.price*x.qty
    context={}
    context['data']=c
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

    #print(c)
    #print(c[0])
    #print(c[0].userid.is_staff)
    

    
def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x == '1':
        q=q+1
    elif q>1:
        q=q-1
    
    c.update(qty=q)
    return redirect('/viewcart')   

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')





def placeorder(request):

    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(orderid=orderid,qty=x.qty,pid=x.pid,
        userid=x.userid,amt=amount)
        o.save()
        x.delete()

    #return render(request,'placeorder.html')
    return redirect('/fetchorder')


def fetchorder(request):
    orders=Order.objects.filter(userid=request.user.id)
    #return HttpResponse("Orders are fetch...")
    sum=0
    for x in orders:
        sum=sum+x.amt
    context={}
    context['data']=orders
    context['total']=sum
    context['n']=len(orders)
    return render(request,'placeorder.html',context)


'''
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_duux1LUL3Ju6du", "gUu1wiUn9rrhvMk5NTrSOXoU"))
    order = Order.objects.filter(userid=request.user.id)
    sum = 0
    for x in order:
        sum=sum+x.amt
        oid=x.orderid
    
    data = { "amount": sum*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context['payment']=payment
    return render(request,'pay.html',context)

    #return HttpResponse("Successfully Paid..!!!")
    '''

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_AtJPLJVMtHFKrz", "TQ9R3eHYG2on1Cb8FH82Rd2e"))

    order = Order.objects.filter(userid=request.user.id)
    sum = 0
    oid=0
    for x in order:
        sum = sum + x.amt
        oid = x.orderid
    
    data = { "amount": sum*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context['payment'] = payment
    #return HttpResponse("Success")
    return render(request,'pay.html',context)



def paymentsuccess(request):
    sub='Ekart-Order Status'
    msg='Thanks For Shopping'
    frm='yadavpranali787@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'paymentsuccess.html')




def search(request):
    context={}
    query=request.GET['query']
    #print(query)
    name=Product.objects.filter(name__icontains=query)
    pdetails=Product.objects.filter(pdetails__icontains=query)
    cat=Product.objects.filter(cat__icontains=query)
    
    allproducts=name.union(pdetails,cat)
    if allproducts.count()==0:
        context['errmsg']=='Products Not Found'

    context['data']=allproducts
    return render(request,'index.html',context)
