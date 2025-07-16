from django.urls import path
from . import views 
from django.contrib.auth import views as auth_view
from .forms import ResetPasswordForm, ChangePasswordForm

urlpatterns = [

    path('',views.homepage,name='homepage'),
    path('category',views.category,name='category'),
    path('viewbycategory/<str:cname>',views.viewbycategory,name='viewbycategory'),
    path('viewproduct/<pid>',views.viewproduct,name='viewproduct'),
    path('signup',views.signup,name='signup'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('userlogout',views.userlogout,name='userlogout'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('updatecartitem',views.updatecartitem,name='updatecartitem'),
    path('removecartitem',views.removecartitem,name='removecartitem'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowishlist',views.addtowishlist,name='addtowishlist'),
    path('removewishlistitem',views.removewishlistitem,name='removewishlistitem'),
    path('checkout',views.checkout,name='checkout'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('makepayment',views.makepayment,name='makepayment'),
    path('myorders',views.myorders,name='myorders'),
    path('vieworder/<str:trackingid>',views.vieworder,name='vieworder'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('productlist',views.productlist,name='productlist'),
    path('searchproduct',views.searchproduct,name='searchproduct'),

    #authviews
    path('password-reset/',
        auth_view.PasswordResetView.as_view(
            template_name='store/password_reset.html',
            subject_template_name='store/password_reset_subject.txt',
            email_template_name='store/password_reset_email.html',
            # success_url='/login/'
            ),
            name='password_reset'),

    path('password-reset/done/',
        auth_view.PasswordResetDoneView.as_view(
            template_name='store/password_reset_done.html'
        ),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_view.PasswordResetConfirmView.as_view(
            template_name='store/password_reset_confirm.html'
        ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_view.PasswordResetCompleteView.as_view(
            template_name='store/password_reset_complete.html'
        ),
        name='password_reset_complete'),


    path('changepassword',auth_view.PasswordChangeView.as_view(template_name='store/changepassword.html',
    form_class=ChangePasswordForm,success_url='/passwordchangedone'),name='changepassword'),

    path('passwordchangedone',auth_view.PasswordChangeDoneView.as_view(template_name='store/passwordchangedone.html'),name='passwordchangedone')

    
]