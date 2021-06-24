from app.forms import LoginForm,PasswordCForm, PasswordRForm, SetPasswordRForm
from django.urls import path
from app import views
from django.contrib.auth import authenticate, views as auth_views

urlpatterns = [
    path('', views.ProductView.as_view(), name = 'home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
   
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.showCart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('miuscart/', views.minus_cart),
    path('removeItem/', views.removeItem),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobileData'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   
   
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name = 'app/changepassword.html', form_class = PasswordCForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class= PasswordRForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class= SetPasswordRForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
   
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
]
