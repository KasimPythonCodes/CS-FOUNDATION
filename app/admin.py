from django.contrib import admin
from app.models import Admin_Post_Img,Evant , User_Contact_Info,CustomUser,Image_Category
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Admin_Post_Img)
admin.site.register(User_Contact_Info)
admin.site.register(Image_Category)
admin.site.register(Evant)


