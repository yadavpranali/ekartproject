from ecomapp import views
from django.urls import path
from ecomapp.views import ContactForm
#from ecomapp.views import Parameter
from django.conf.urls.static import static
from django.conf import settings

'''
    path('about',views.about),
    path('delete/<rid>',views.delete),
    path('edit/<name>',views.edit),
    path('contact',ContactForm.as_view()),
    path('para/<cid>',Parameter.as_view()),
    path('hello',views.hello),
    path('message',views.message),
    path('base',views.base),
    
    path('contact',views.contact),
    '''
urlpatterns = [
    path('about',views.about),
    path('contact',views.contact),
    path('products',views.products),
    #path('register',views.register),
    #path('login',views.user_login),
    path('logoutpage',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('filterbyprice',views.filterbyprice),
    path('product_details/<pid>',views.product_detail),
    path('addcart/<pid>',views.cart),
    #path('login',views.login)
    path('registerpage',views.register),
    path('loggedin',views.user_login),
    path('viewcart',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart/<cid>',views.removecart),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('search',views.search),
    
] 

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)