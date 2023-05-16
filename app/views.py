from django.shortcuts import render , HttpResponse ,redirect
from app.models import*
from django.views import View
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login ,  logout ,authenticate 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import time
from django.db.models import Q 
import datetime
import csv
from django.core.exceptions import ValidationError
# Create your views here.


@csrf_exempt
def search(request):
    get_info=CustomUser.objects.all()
    contact_data=User_Contact_Info.objects.all()
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            contact_data=User_Contact_Info.objects.filter(Q(full_name__icontains=query)|Q(user_email__icontains=query))
            obj_e =Evant.objects.all() 
            return render(request, "Admin_Templates\search_contact_user_data.html",{'obj_e':obj_e,'contact_data':contact_data,'get_info':get_info,'query':query})

        elif query=='':
            obj_e =Evant.objects.all() 
            return render(request, "Admin_Templates\search_contact_user_data.html",{'obj_e':obj_e,'contact_data':contact_data,'get_info':get_info,'query':query})
        else:
            obj_e =Evant.objects.all() 
            return render(request, "Admin_Templates\search_contact_user_data.html",{'obj_e':obj_e,'get_info':get_info,'query':query})

def Download(request,download_id):
    response = HttpResponse(content_type = 'text/csv')
    #response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename = user_file_download'+ str(datetime.datetime.now())+'.csv'
    down_list = User_Contact_Info.objects.filter(id=download_id)
    writer = csv.writer(response)
    # writer.writerow(['User Id', 'Ref ID', 'User Name', 'Amount'])
    writer.writerow(['full_name' ,'user_email' ,'phone_no','subject','message_info'])
    for approve in down_list:
        print(approve)
        writer.writerow(
                [
				approve.full_name, 
				approve.user_email, 
				approve.phone_no, 
				approve.subject, 
				approve.message_info, 

                ])
           
        return response

def Admin_Page(request):
    get_info=CustomUser.objects.all()
    obj_e =Evant.objects.all() 
    return render(request , "Admin_Templates/index.html",{'obj_e':obj_e,'get_info':get_info})

def User_Contact_for_Admin(request):
    conatct_data=User_Contact_Info.objects.all().order_by('id')
    conatct_data_count=User_Contact_Info.objects.all().count()
    get_info=CustomUser.objects.all()
    paginator = Paginator(conatct_data , 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
         page_obj = paginator.page(paginator.num_pages)
    view = paginator.get_page(page_number)
    obj_e =Evant.objects.all() 
    return render(request , "Admin_Templates/contactdata.html",{'obj_e':obj_e,'conatct_data':conatct_data,'get_info':get_info,'page_obj':view,'conatct_data_count':conatct_data_count})    

def User_Contact_for_Admin_Delete(request , contact_id):
    obj=User_Contact_Info.objects.get(id=contact_id)
    obj.delete()
    messages.success(request, "User Contact deleted")
    return redirect(User_Contact_for_Admin)

def Admin_Post(request):
    if request.method =='POST':
        category_name_id=request.POST.get('category_name')
        galary_img=request.FILES.get('galary_img')
        if not str(galary_img).split('.')[-1].lower() in ["jpg","jpeg","png","gif"]:
                messages.error(request , "File format  supported, please try again and upload a JPG/PNG/GIF file")
        else:
            cate_obj=Image_Category.objects.get(id=category_name_id)
            obj=Admin_Post_Img(Img_Avatar = galary_img ,select_category=cate_obj)
            obj.save()
            messages.success(request , "Your Post successfully Uplaod")
    get_info=CustomUser.objects.all()
    get_img_category=Image_Category.objects.all()
    obj_e =Evant.objects.all()  
    return render(request , "Admin_Templates/galary_post.html",{'get_info':get_info,'get_img_category':get_img_category ,'obj_e':obj_e})    

def Admin_Post_View(request):
    IMG=Admin_Post_Img.objects.all().order_by('id')
    get_info=CustomUser.objects.all()
    paginator = Paginator(IMG , 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
         page_obj = paginator.page(paginator.num_pages)
    view = paginator.get_page(page_number)
    obj_e =Evant.objects.all()  
    return render(request , "Admin_Templates/view_post.html",{'img_a':IMG,'get_info':get_info,'page_obj': view,'obj_e':obj_e})    

def Admin_Post_Delete(request , post_id):
    Img_delete=Admin_Post_Img.objects.get(id = post_id)
    Img_delete.delete()
    messages.success(request , "Your Post Deleted")
    return redirect(Admin_Post_View)

def Admin_Post_Edit(request,edit_id):
    Img_edit=Admin_Post_Img.objects.get(id=edit_id)
    get_info=CustomUser.objects.all()
    obj_e =Evant.objects.all()  
    return render(request, 'Admin_Templates/update_post.html',{'Img_edit':Img_edit,'get_info':get_info,'obj_e':obj_e})

def Admin_Update(request):
    img_id=request.POST.get('id_img')
    update_img=Admin_Post_Img.objects.get(id=img_id)
    if request.method=='POST':
        # img_id=request.POST.get('id_img')
        img_update=request.FILES.get('galary_img_update')
        if not str(img_update).split('.')[-1].lower() in ["jpg","jpeg","png","gif"]:
                messages.error(request , "File format  supported, please try again and upload a JPG/PNG/GIF file")
                return redirect(Admin_Post_View)    
        else:
            update_img.Img_Avatar=img_update
            update_img.save()
            messages.success(request, "Your record successfully updated")
            return redirect(Admin_Post_View)
    get_info=CustomUser.objects.all()
    obj_e =Evant.objects.all()  
    return render(request, 'Admin_Templates/update_post.html',{'get_info':get_info,'obj_e':obj_e})

def Admin_Create_Category(request):
    if request.method=='POST' :
        current_user = request.user
        create_category = request.POST.get('create_category')
        if Image_Category.objects.filter(create_category=create_category).exists():
            messages.warning(request, "This Category Already Exists")
            return redirect(Admin_Create_Category)
        Image_Category(create_category=create_category ,user=current_user).save()
        messages.success(request, "Your Category successfully Create")
        return redirect(Admin_Create_Category)
    get_info=CustomUser.objects.all()  
    obj_e =Evant.objects.all()  
    return render(request, 'Admin_Templates/admin_create_category.html',{'get_info':get_info,'obj_e':obj_e})

def Admin_Category_View(request):
    views_category=Image_Category.objects.all()
    get_info=CustomUser.objects.all()   
    obj_e =Evant.objects.all()
    return render(request, "Admin_Templates/admin_view_category.html",{"views_category":views_category,'get_info':get_info,'obj_e':obj_e})

def Admin_Category_Delete(request, cate_id):
    cate_id=Image_Category.objects.get(id=cate_id)
    cate_id.delete()
    messages.success(request , "Your Category Deleted")
    return redirect(Admin_Category_View)

def  Admin_Category_Edit(request,category_id):
    obj_update=Image_Category.objects.get(id=category_id)
    obj_e=Evant.objects.all() 
    return render(request, 'Admin_Templates/admin_category_edit.html',{'obj_update':obj_update,'obj_e':obj_e})

def Admin_Category_Update(request):
    cate_id = request.POST.get('id_category')
    # print(cate_id,"kkkkkkkkkkkkkkkkkkkkk")
    if request.method == 'POST':
        current_user =request.user
        cate_name= request.POST.get('category_name')
        obj_cate=Image_Category.objects.get(id=cate_id)
        obj_cate.create_category=cate_name
        obj_cate.user=current_user                                                             
        obj_cate.save()
        messages.success(request,  "Your Category Successfully Updated !!")
        return redirect(Admin_Category_View)
    obj_e=Evant.objects.all() 
    return render(request, 'Admin_Templates/admin_update.html' ,{'obj_e':obj_e})

def User_Admin_Update_Profile(request , Profile_id):
    get_id=CustomUser.objects.get(id=Profile_id)
    get_info=CustomUser.objects.all()
    obj_e=Evant.objects.all()   
    return render(request, 'Admin_Templates/admin_update.html',{'get_info':get_info,'get_id':get_id,"obj_e":obj_e})

def User_Admin_Finaly_Update_Profile(request):
    if request.method == 'POST':
        current_admin_id=request.POST.get('admin_id')
        user_pic=request.FILES.get('admin_galary_img')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(current_admin_id ,user_pic ,first_name ,last_name ,email,password,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        update_admin=CustomUser.objects.get(id=current_admin_id)
        update_admin.first_name=first_name
        update_admin.last_name=last_name
        # update_admin.email=email
        # update_admin.password=password
        if password !=None and password != "":
            update_admin.set_password(password)
        if user_pic != None and user_pic !="":
            update_admin.profile_pic = user_pic
        update_admin.save()    
        return   redirect('/s-admin/')
        messages.success(request,  "Your Profile Successfully Updated !!")
    obj_e=Evant.objects.all()    
    return render(request, 'Admin_Templates/admin_update.html',{'obj_e':obj_e})

def User_About(request):
    return render(request, 'User_Templates/about.html')

def User_Causes(request ,data=None):
    galary_imgs=Admin_Post_Img.objects.all().order_by('id')
    pro_cate = Image_Category.objects.all()
    cate = request.GET.get(str('category'))
    # print(cate,"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    pro_img = Admin_Post_Img.objects.filter(select_category__create_category=cate) 
    paginator = Paginator(galary_imgs , 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
         page_obj = paginator.page(paginator.num_pages)
    view = paginator.get_page(page_number)
    return render(request, 'User_Templates/causes.html',{'galary_imgs':galary_imgs,'page_obj':view,'pro_cate':pro_cate ,'pro_img':pro_img})   


# def Galary(request ,data=None):
#     galary_pics=Admin_Post_Img.objects.all()
#     galary_img=Image_Category.objects.all()
#     category_sec = request.GET.get(str('category'))
#     if data==None:
#         galary_pics=Admin_Post_Img.objects.all()
#     galary_pic=Admin_Post_Img.objects.filter(select_category_id=category_sec)
#     return render(request, 'User_Templates/allcauses.html',{'galary_pic':galary_pic,'galary_pics':galary_pics,'galary_img':galary_img})   


def User_Contact(request):
    if request.method == 'POST':
        full_name= request.POST.get('Full_Name')
        email= request.POST.get('email')
        phone_no= request.POST.get('phone_no')
        subject= request.POST.get('subject')
        message_info= request.POST.get('message_info')
        obj=User_Contact_Info(full_name=full_name ,user_email=email ,phone_no=phone_no,subject=subject,message_info=message_info)
        if User_Contact_Info.objects.filter(user_email=email).exists():
            messages.warning(request, "This Email Already Exists")
            return redirect("User_Contact") 

        elif User_Contact_Info.objects.filter(phone_no=phone_no).exists():
            messages.warning(request, "This Phone Already Exists")
            return redirect("User_Contact")  

        obj.save()
        messages.success(request, "Your Query Successfully Submited")
    return render(request, 'User_Templates/contact.html')

def User_Donation(request):
    return render(request, 'User_Templates/donation.html')

def User_Education(request):
    return render(request, 'User_Templates/Education.html')

def User_Eventdetails(request):
    obj=Evant.objects.all()
    obj_e=Evant.objects.all()
    return render(request, 'User_Templates/event-details.html',{'obj':obj,'obj_e':obj_e})

def User_Evant_post(request):
    if request.method == 'POST':
        img = request.FILES.get('img_evant')
        obj=Evant(img_evant = img)
        obj.save()
        messages.success(request,  "Your Evant Img Successfully Post !")
        return redirect(User_Evant_post)
    obj_e=Evant.objects.all()
    get_info=CustomUser.objects.all()
    return render(request, 'Admin_Templates/evant_post.html',{'obj_e':obj_e,'get_info':get_info})
    
def User_Evant_post_Edit(request ,id):
    obj=Evant.objects.get(id=id)
    obj_e=Evant.objects.all()
    get_info=CustomUser.objects.all()
    return render(request, 'Admin_Templates/evant_post.html',{'obj':obj ,'obj_e':obj_e,'get_info':get_info})

def user_Evant_Update(request):
    if request.method == 'POST':
        galary_img_id = request.POST.get('galary_img_id')
        print(galary_img_id,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        img_evant = request.FILES.get('img_evant')  
        obj = Evant.objects.get(id=galary_img_id)    
        obj.img_evant=img_evant
        obj.save()
        messages.success(request,  "Your Evant Image Successfully Update !")
        return redirect(f'/Admin-Evant-edit/{galary_img_id}')
    get_info=CustomUser.objects.all()
    return render(request, 'Admin_Templates/evant_post.html',{'get_info':get_info})
    

def User_Events(request):
    return render(request, 'User_Templates/events.html')

def User_Faq(request):
    return render(request, 'User_Templates/faq.html')

def User_Health(request):
    return render(request, 'User_Templates/health.html')

def User_Index(request):
    return render(request, 'User_Templates/index.html')

def User_Marriage(request):
    return render(request, 'User_Templates/marriage.html')

def User_Newsdetails(request):
    return render(request, 'User_Templates/news-details.html')

def User_Outproduct(request):
    return render(request, 'User_Templates/ourproduct.html')

def User_Team(request):
    return render(request, 'User_Templates/team.html')





class Email_With_Login_User(ModelBackend):
    def authenticate(self , username=None , password=None , **kwargs):
        CustomUser = get_user_model()
        try:
            user= CustomUser.objects.get(email = username)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

def User_login(request):
    if request.method == 'POST':
        user = Email_With_Login_User.authenticate(request, username=request.POST.get('email') , password=request.POST.get('password'),)
        if user != None:
            login(request, user)
            return redirect('/s-admin/')
        else:
            messages.error(request , "Email or Password are Invalid !")
            return redirect('admin_login')
    else:
        pass
    return render(request , 'Admin_Templates/admin_login.html')    

    # if request.method == 'POST':
    #     user = Email_With_Login_User.authenticate(request, username=request.POST.get('email') , password=request.POST.get('password'),)
    #     if user != None:
    #         login(request , user)
    #         return redirect('/s-admin/')
    #     else:
    #         messages.error(request , "Email or Password are Invalid !")
    #         return redirect('admin_login')
    # else:
    #     return redirect('admin_login')      
    # return render(request , 'Admin_Templates/admin_login.html')    
    
def logout_user(request):
    logout(request)
    return redirect('/')    