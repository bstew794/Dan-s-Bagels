from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='bagels/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='bagels/password_reset_form.html',
                                                                email_template_name='bagels/password_reset_email.html',
                                                                subject_template_name='bagels/password_reset_subject.txt',
                                                                from_email='bstewart794Agmail.com',
                                                                ), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='bagels/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='bagels/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='bagels/password_reset_complete.html'),
         name='password_reset_complete'),
    path('current_orders', views.CurrentOrderListView.as_view(), name='current_orders'),
    path('fulfill_order/<int:order_id>/', views.fulfillOrder, name='fulfill_order'),
    path('prepare_order/<int:order_id>/', views.prepareOrder, name='prepare_order'),
]
