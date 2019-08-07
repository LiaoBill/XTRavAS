from django.urls import path

from . import views

urlpatterns = [
    path('', views.showMainPage, name='show_main_page'),
    path('login', views.admin_login, name="admin_login"),
    path('mf', views.showMainFunctionPage, name="main_function_page"),
    path('uscenter', views.showUserCenter, name="user_center"),
    path('upheadp', views.updateUserHeadPortrait, name='update_head_portrait'),
    path('hprl', views.headportrait_rotate_left, name='headportrait_rotate_left'),
    path('hprr', views.headportrait_rotate_right, name='headportrait_rotate_right'),
    path('addmo', views.addMoneyObject, name='add_moneyObject'),
    path('motpday/<str:trip_day>', views.showMO_tripday, name='show_mo_tripday'),
    path('mo/<str:mo_id>', views.showMO_spec, name='show_mo_spec'),
    path('userv/<str:username>', views.showUserView, name='show_user_view'),
    path('upmo/<str:mo_id>', views.updateMoneyObject, name='update_moneyObject'),
    # path('upmoimg/<str:mo_id>', views.updateMoneyObjectImage, name='update_moneyObject_image'),
    path('newmoimg/<str:mo_id>', views.newMoneyObjectImage, name='new_moneyObject_image'),
    path('updtripinfo', views.updateTripInfo, name='update_trip_info'),
    path('deletemo/<str:mo_id>', views.deleteMO, name='delete_money_object'),

    path('logout', views.admin_logout, name='admin_logout'),
]