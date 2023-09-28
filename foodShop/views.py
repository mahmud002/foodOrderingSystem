from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from .models import *
from .forms import *
import os
from django.conf import settings
import json
from django.shortcuts import render, get_object_or_404
import json

from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO

# Create your views here.
def index(request):
    
    return render(request,'home.html')

##Profile Section
def profile(request):
    if request.user.is_authenticated:
        profile_data = Profile.objects.get(user=request.user)
        order_request=Order.objects.filter(owner=request.user,status="not_taken")
        order_accepted=Order.objects.filter(owner=request.user,status="accepted")
        food_items_by_category = {}
        for food_item in profile_data.food_list:
            category = food_item["category"]
            if category not in food_items_by_category:
                food_items_by_category[category] = []
            food_items_by_category[category].append(food_item)

        n=int(profile_data.number_of_table)
        url_list=[]
        i=1
        while(i<=n):
            url_list.append({'name':"Table "+str(i),'url':"/catalog/"+str(profile_data.user)+"?table="+str(i)})
            i=i+1

        return render(request,'profile.html',{'profile_data':profile_data, 'url':url_list, 'order':order_request,'order_accepted':order_accepted,'food_items_by_category':food_items_by_category })
    else:
        return render(request,'login.html')

def order_list(request):
    if request.user.is_authenticated:
        profile_data = Profile.objects.get(user=request.user)
        order_request=Order.objects.filter(owner=request.user,status="not_taken")
        order_accepted=Order.objects.filter(owner=request.user,status="accepted")
        

        return render(request,'order_list.html',{'profile_data':profile_data, 'order':order_request,'order_accepted':order_accepted })
    else:
        return render(request,'login.html')
def edit_profile (request):
        if request.user.is_authenticated:

            if request.method=='POST':
                pi=Profile.objects.get(user=request.user)
                profile = request.user.profile
                if profile.logo_image:
                    # Delete the previous image from storage
                    default_storage.delete(profile.logo_image.path)
                    print("Delete Logo______________________")

                fm=ProfileForm(request.POST, request.FILES,instance=pi)
                if fm.is_valid:
                    fm.save()
                    return redirect('profile')

            else:
                pi=Profile.objects.get(user=request.user)
                
                fm=ProfileForm(instance=pi)

            return render(request,'profile_edit.html',{'form':fm})

        else:
            return HttpResponse("Please Login First")

# def insert_food(request):
#     if request.user.is_authenticated:       
#         form=FoodForm()
#         pi=Profile.objects.get(user=request.user)
#         data = pi.food_list


#         if request.method =='POST':
#             form=FoodForm(request.POST,request.FILES)
#             index=0
#             index_list=[]
#             for i in data:
#                 index_list.append(int(i['index']))
    
#             while index in index_list:
#                 print(index)
#                 index=index+1
   
#             if form.is_valid():
#                 new_object = {
#                     'index':index,
#                     'food_title': str(form.cleaned_data['food_title']),
#                     'food_price': str(form.cleaned_data['food_price']),
#                     'category': str(form.cleaned_data['category']),
#                     'description': str(form.cleaned_data['description']),
#                     'food_image' : "home/images/"+str(form.cleaned_data['food_image']).replace(' ','_')
#                 }
#                 full_path = os.path.join(settings.MEDIA_ROOT, new_object['food_image'])
#                 image_file = form.cleaned_data['food_image']
#                 image_data = image_file.read()
#                 with open(full_path, 'wb') as f:
#                     f.write(image_data)


                
#                 data.append(new_object)
#                 pi.food_list = data
#                 pi.save()
                
#                 # instance.username=request.user.profile
#                 # form.save()
               
#             return redirect('profile')
#         return render(request,'food_form.html',{'form':form})
#     else:
#         return HttpResponse("Please Login First")



def resize_image(image_file, max_size=(800, 600)):
    img = Image.open(image_file)
    img.thumbnail(max_size)
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=85)
    img_io.seek(0)
    return img_io
def insert_food(request):
    if request.user.is_authenticated:
        form = FoodForm()
        pi = Profile.objects.get(user=request.user)
        data = pi.food_list

        if request.method == 'POST':
            form = FoodForm(request.POST, request.FILES)
            index = 0
            index_list = []

            for i in data:
                index_list.append(int(i['index']))

            while index in index_list:
                index = index + 1

            if form.is_valid():
                # Resize the image before saving
                resized_image = resize_image(form.cleaned_data['food_image'])

                # Generate a unique filename for the resized image
                unique_filename = "home/images/"+str(index)+"_"+str(form.cleaned_data['food_image']).replace(' ', '_')

                # Save the resized image to the file system
                full_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
                with open(full_path, 'wb') as f:
                    f.write(resized_image.read())

                # Save the URL of the resized image in your Profile object
                new_object = {
                    'index': index,
                    'food_title': str(form.cleaned_data['food_title']),
                    'food_price': str(form.cleaned_data['food_price']),
                    'category': str(form.cleaned_data['category']),
                    'description': str(form.cleaned_data['description']),
                    'food_image': unique_filename  # Store the URL here
                }

                data.append(new_object)
                pi.food_list = data
                pi.save()
               
            return redirect('profile')
        return render(request,'food_form.html',{'form':form})
    else:
        return HttpResponse("Please Login First")
def find_dictionary_by_data(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if dictionary.get(key) == value:
            return dictionary
    return None
def update_food(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            py_food=Food()
            pk=Profile.objects.get(user=request.user)

            if request.POST.get('form_type') == 'identifire':
                product_id=request.POST['product_id']
                food_list=pk.food_list
                
                food=find_dictionary_by_data(food_list, "food_title", product_id)
                py_food.index=food['index']
                py_food.food_title=food['food_title']
                py_food.food_price=food['food_price']
                py_food.category=food['category']
                py_food.description=food['description']
                py_food.food_image=food['food_image']

 
                form=FoodForm(instance=py_food)
                
                return render(request,'food_edit_form.html',{'form':form})
            else:
                form=FoodForm(request.POST, request.FILES, instance=py_food)
                if form.is_valid():                    
                    food_list=pk.food_list

                    
                    food=None
                    for i in food_list:
                        if int(i['index'])==int(form.cleaned_data['index']):
                            food=i
                    food['food_title']=form.cleaned_data['food_title']
                    food['food_price']=form.cleaned_data['food_price']
                    food['category']=form.cleaned_data['category']
                    food['description']=form.cleaned_data['description']
                    clear=form.cleaned_data['clear_image_url']

    
                    
                    if clear:
                        default_storage.delete(food['food_image'])
                        food['food_image']=""
                    # elif not form.cleaned_data['food_image'] :
                    #     food['food_image']=food['food_image']
                    
                    else:
                        default_storage.delete(food['food_image'])

                        
                        resized_image = resize_image(form.cleaned_data['food_image'])

                        # Generate a unique filename for the resized image
                        unique_filename = "home/images/"+str(food['index'])+"_"+str(form.cleaned_data['food_image']).replace(' ', '_')

                        # Save the resized image to the file system
                        full_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
                        with open(full_path, 'wb') as f:
                            f.write(resized_image.read()) 
                        food['food_image']=unique_filename
                        # full_path = os.path.join(settings.MEDIA_ROOT, food['food_image'])
                        # image_file = form.cleaned_data['food_image']
                        # image_data = image_file.read()
                        # with open(full_path, 'wb') as f:
                        #     f.write(image_data)
                    pk.save()
                    
 
    return redirect('profile')


def delete_food(request):
    if request.user.is_authenticated:
        pk=Profile.objects.get(user=request.user)
        product_id=request.POST['product_id']
        food_list=pk.food_list
        food=find_dictionary_by_data(food_list, "food_title", product_id)
        
                    # Delete the previous image from storage
        default_storage.delete(food['food_image'])
        print("Delete Food Image______________________")
        food_list.remove(food)
        pk.food_list=food_list
        pk.save()
    return redirect('profile')

def catalog(request,key):
    user = get_object_or_404(User, username=key)
    food_list=Profile.objects.filter(user=user).values('food_list').first()['food_list']
    
    food_items_by_category = {}
    for food_item in food_list:
        category = food_item["category"]
        if category not in food_items_by_category:
            food_items_by_category[category] = []
        food_items_by_category[category].append(food_item)
    resturant_Name=Profile.objects.values('resturant_name').get(user=user)
    
    table_no = request.GET.get('table')

    return render(request,'catalog.html',{'food_items_by_category':food_items_by_category,'key':key,'resturantName':resturant_Name['resturant_name'],'table_no':table_no})

def accept_order (request):
    if request.method=='POST':
        id=request.POST['order_id']
        order=Order.objects.get(id=id)
        order.status="accepted"
        order.save()
        return redirect("order_list")

def submit_order(request):
    if request.method == 'POST':
        # Process the submitted data
        cart_items = request.POST.get('data')  # Access the submitted data
        data=json.loads(cart_items)
        # key=get_object_or_404(User, username=data[0]['key'])

        user=User.objects.get(username=data['owner'])
        new_order=Order(owner=user,food_list=data['cartItems'],table_no=data['table_no'],customer_phone_number=data['phone'],order_password=data['order_password'],status="not_taken")
        
      
        new_order.save()
  
        
        return redirect("/catalog/"+data['owner'])
   
##Login Logout
def login (request):
    if request.method=='POST':
        username1=request.POST['username']
        password1=request.POST['password']

        user=authenticate(username=username1,password=password1)

        if user is None:
            return redirect('login')            
        else: 
            if Profile.objects.filter(user=user).exists():
                pass
            else:
                new_pro=Profile(user=user)
                new_pro.save()
                
            
            auth.login(request, user)
            return redirect('/')
            
    
    else:    
         return render(request,'login.html')



   
def logout (request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    else:
        return HttpResponse("Please Login First")
def signup (request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # new_pro=Profile(user=request.user)
            # new_pro.save()
            return redirect('login')
    else:
        form=UserCreationForm()
    return render (request,'singup.html',{'form': form})

def update_password (request):
    if request.method == 'POST':
        username_to_update = request.POST['username']  # Get the username from the form
        new_password = request.POST['new_password']  # Get the new password from the form

        try:
            user = User.objects.get(username=username_to_update)
        except User.DoesNotExist:
            return redirect('error_view')  # Handle the case where the user doesn't exist

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return redirect('profile')  # Redirect to a success view or page

    return render(request, 'update_password_form.html')  # Render the password update form