
from django.urls import path
from foodShop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index,name='index'),
    path("profile",views.profile,name='profile'),
    path("catalog/<str:key>",views.catalog,name="catalog"),
    path("login",views.login,name="login"),
    path("signup",views.signup,name="signup"),
    path("logout",views.logout,name="logout"),
    path("edit_profile",views.edit_profile, name='edit_pro'),
    path("insert_food",views.insert_food, name='insert_food'),
    path("update_food",views.update_food, name='update_food'),
    path("delete_food",views.delete_food, name='update_food'),
    path("submit_order",views.submit_order, name='submit_order'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
