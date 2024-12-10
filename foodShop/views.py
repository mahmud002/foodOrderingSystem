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
from django.http import JsonResponse
from django.core.files.storage import default_storage
from PIL import Image, ImageOps
from io import BytesIO
from datetime import datetime, timedelta

import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
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

        if profile_data.number_of_table is not None:
            n = int(profile_data.number_of_table)
        else:
            n=0
        url_list=[]
        i=1
        while(i<=n):
            url_list.append({'name':"Table "+str(i),'url':"http://127.0.0.1:8000/catalog/"+str(profile_data.user)+"?table="+str(i)})
            i=i+1

        return render(request,'profile.html',{'profile_data':profile_data, 'url':url_list, 'order':order_request,'order_accepted':order_accepted,'food_items_by_category':food_items_by_category })
    else:
        return render(request,'login.html')

    


def order_list(request):
    if request.user.is_authenticated:
        profile_data = Profile.objects.get(user=request.user)
        order_request=Order.objects.filter(owner=request.user,status="not_taken")
        order_accepted=Order.objects.filter(owner=request.user,status="accepted")
        this_week=""
        this_month=""

        return render(request,'order_list.html',{'profile_data':profile_data, 'order':order_request,'order_accepted':order_accepted, 'yesterday': datetime.now()- timedelta(days=1)})
    else:
        return render(request,'login.html')
# def edit_profile (request):
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

def edit_profile(request):
    if request.user.is_authenticated:
        # Fetch the user's profile
        profile = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            # When the form is submitted
            
            # Save the previous image before the update, if needed
            if 'logo_image-clear' in request.POST and profile.logo_image:
                # If the user wants to clear the logo image, delete the old image
                default_storage.delete(profile.logo_image.path)
                profile.logo_image = None  # Remove the image from the profile
                profile.save()
                print("Previous logo image deleted.")

            # Initialize the form with the POST data and the current profile instance
            form = ProfileForm(request.POST, request.FILES, instance=profile)

            if form.is_valid():  # Corrected form validation
                form.save()  # Save the updated profile
                return redirect('profile')  # Redirect to the profile view page

        else:
            # When the form is first opened (GET request)
            form = ProfileForm(instance=profile)
            
        return render(request, 'profile_edit.html', {'form': form})

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



# def resize_image(image_file, max_size=(800, 600)):
#     img = Image.open(image_file)
#     img.thumbnail(max_size)
#     img_io = BytesIO()
#     img.save(img_io, format='JPEG', quality=85)
#     img_io.seek(0)
#     return img_io

def resize_image(image_file):
    image = Image.open(image_file)
    
    # Desired max width and height based on CSS
    desired_width = 500
    desired_height = 370
    
    # Resize the image while maintaining its aspect ratio
    image = ImageOps.fit(image, (desired_width, desired_height), method=0, bleed=0.0, centering=(0.5, 0.5))
    
    return image
    # image = Image.open(image_file)
    # image = image.resize((200, 200))  # Adjust width and height as needed
    # return image

    # image = Image.open(image_file)
    
    # # Get the original image's aspect ratio
    # width, height = image.size
   
    # # Desired max width and height based on CSS
    # desired_width = 500
    # desired_height = 370
    
    # # Aspect ratio of the original image
    # aspect_ratio = width / height
    
    # # Resize while maintaining aspect ratio
    # if aspect_ratio >= 1:  # Landscape or square image
    #     # Resize width to 250px, height will scale proportionally
    #     new_width = desired_width
    #     new_height = int(desired_width / aspect_ratio)
    # else:  # Portrait image
    #     # Resize height to 295px, width will scale proportionally
    #     new_height = desired_height
    #     new_width = int(desired_height * aspect_ratio)
    
    # # Resize the image
    # resized_image = image.resize((new_width, new_height))
    
    # # Now crop to desired dimensions (250px x 295px)
    # left = (new_width - desired_width) // 2
    # top = (new_height - desired_height) // 2
    # right = left + desired_width
    # bottom = top + desired_height
    
    # cropped_image = resized_image.crop((left, top, right, bottom))
    
    # return cropped_image

def insert_food(request):
    if request.user.is_authenticated:
 
        pi = Profile.objects.get(user=request.user)
        
        data = pi.food_list
        unique_categories = set(item['category'] for item in data)

    # Pass the unique categories to the form
        form = FoodForm()  # Initialize the form without 'categories' argument

        context = {
            'form': form,
            'unique_categories': unique_categories,  # Pass categories to the template
        }

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
                # Resize and crop the uploaded image
                resized_image = resize_image(form.cleaned_data['food_image'])

                # Generate a unique filename for the resized image
                unique_filename = f"home/images/{index}_{str(form.cleaned_data['food_image']).replace(' ', '_')}"

                # Define the full file path for saving the image
                full_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

                # Save the resized image to the file system
                with open(full_path, 'wb') as f:
                    resized_image.save(f, format='JPEG')  # Saving as JPEG, you can choose another format if necessary

                # Prepare data to store in the profile
                new_object = {
                    'index': index,
                    'food_title': str(form.cleaned_data['food_title']),
                    'food_price': str(form.cleaned_data['food_price']),
                    'category': str(form.cleaned_data['category']),
                    'description': str(form.cleaned_data['description']),
                    'food_image': unique_filename  # Store the URL here
                }

                # Append the new object to the data list
                data = pi.food_list if pi.food_list else []
                data.append(new_object)

                # Save the updated food list back to the profile
                pi.food_list = data
                pi.save()

                # Redirect to the profile page
                return redirect('profile')
        
        return render(request,'food_form.html',context)
    else:
        return HttpResponse("Please Login First")
def find_dictionary_by_data(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if dictionary.get(key) == value:
            return dictionary
    return None
# Resize the image (adjust the size as needed)

def update_food(request):
    if request.user.is_authenticated:
        
        if request.method=='POST':
            py_food=Food()
            
            pk=Profile.objects.get(user=request.user)

            if request.POST.get('form_type') == 'identifire':
                product_id=request.POST['product_id']
                print(product_id)
                print("_____________________________________________")
                food_list=pk.food_list
                
                food=find_dictionary_by_data(food_list, "index", int(product_id))
                
                py_food.index=food['index']
                py_food.food_title=food['food_title']
                py_food.food_price=food['food_price']
                py_food.category=food['category']
                py_food.description=food['description']
                py_food.food_image=food['food_image']
                data = pk.food_list
                unique_categories = set(item['category'] for item in data)
                form=FoodForm(instance=py_food)
                context = {
                'form': form,
                'unique_categories': unique_categories,  # Pass categories to the template
                'index':py_food.index,
                'category_selected':food['category'],
                'food_image':food['food_image']
                
                }
                
                
                return render(request,'food_edit_form.html',context)
            else:
                form=FoodForm(request.POST, request.FILES, instance=py_food)
                if form.is_valid():                    
                    food_list=pk.food_list
                    food=None
                    index=form.cleaned_data['index']

             
                    for i in food_list:
                        if int(i['index'])==int(form.cleaned_data['index']):
                            food=i
                    food['food_title']=form.cleaned_data['food_title']
                    food['food_price']=form.cleaned_data['food_price']
                    food['category']=form.cleaned_data['category']
                    food['description']=form.cleaned_data['description']
                    

    
                    clear=form.cleaned_data['pre_food_image']
                    if form.cleaned_data['food_image']==None:
                    #     default_storage.delete(food['food_image'])
                    #     food['food_image']=""
                    # elif not form.cleaned_data['food_image'] :
                        food['food_image']=clear
                        print("Working______________________")
                    
                    else:
                        default_storage.delete(clear)
                        # resized_image = resize_image(form.cleaned_data['food_image'])

                        # # Generate a unique filename for the resized image
                        # unique_filename = "home/images/"+str(food['index'])+"_"+str(form.cleaned_data['food_image']).replace(' ', '_')

                        # # Save the resized image to the file system
                        # full_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
                        # with open(full_path, 'wb') as f:
                        #     f.write(resized_image.read()) 
                        # food['food_image']=unique_filename


                        # Your form.cleaned_data logic
                        uploaded_image = form.cleaned_data['food_image']

                        # Generate a unique filename
                        # Get the file extension from the uploaded image
                        file_extension = uploaded_image.name.split('.')[-1].lower()

                        # Ensure the file has a valid extension (can add more if necessary)
                        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
                        if file_extension not in valid_extensions:
                            raise ValueError("Invalid image format")

                        # Generate a unique filename using the extension
                        unique_filename = f"home/images/{food['index']}_{uploaded_image.name.replace(' ', '_')}"

                        # Save the resized image to the file system
                        full_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

                        # Resize the image
                        resized_image = resize_image(uploaded_image)

                        # Save the image with the correct extension
                        resized_image.save(full_path)

                        # Update food image path
                        food['food_image'] = unique_filename








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
        food=find_dictionary_by_data(food_list, "index", int(product_id))
        
                    # Delete the previous image from storage
        default_storage.delete(food['food_image'])
        print("Delete Food Image______________________")
        food_list.remove(food)
        pk.food_list=food_list
        pk.save()
    return redirect('profile')

def catalog(request,key):
    if request.COOKIES.get('food_order_email'):

        user = get_object_or_404(User, username=key)
        food_list=Profile.objects.filter(user=user).values('food_list').first()['food_list']
        
        food_items_by_category = {}
        for food_item in food_list:
            category = food_item["category"]

            if category not in food_items_by_category:
                food_items_by_category[category] = []
            food_items_by_category[category].append(food_item)
        
        # If "Offer" is in the dictionary, move it to the front
        if "Offer" in food_items_by_category:
            offer_items = food_items_by_category.pop("Offer")
            food_items_by_category = {"Offer": offer_items, **food_items_by_category}

        resturant_Name=Profile.objects.values('resturant_name').get(user=user)
        

        table_no = request.GET.get('table')
        customer= request.COOKIES.get('food_order_email')
        print(customer)
        return render(request,'catalog.html',{'customer_email':customer,'food_items_by_category':food_items_by_category,'key':key,'resturantName':resturant_Name['resturant_name'],'table_no':table_no})
    else:
        next_url = request.get_full_path()
        return redirect(f'/customer_login/?next={next_url}')
     

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
        new_order=Order(owner=user,food_list=data['cartItems'],table_no=data['table_no'],email=data['phone'],status="not_taken",total=data['total'],created_at=datetime.now())
        
 
       
        new_order.save()
        new_object_id = new_order.id
        redirect_url = '/order_status'  # Replace with the actual URL of your new page

        # Return a JSON response with the redirect URL
        response_data = {'redirect_url': redirect_url}
        response = JsonResponse(response_data)

    # Set a cookie in the response
        response.set_cookie('food_order_cookie', new_object_id, max_age=43200)

        return response

def order_status(request):
    if request.COOKIES.get('food_order_cookie'):
        id=request.COOKIES.get('food_order_cookie')
        order=Order.objects.get(id=id)
        print(id)
        print("__________________________")
        return render(request,'order_status.html',{'order':order, 'token_number':id})
    else:
        return HttpResponse("You not ordered")

def reject_order(request):
    if request.method=='POST':
        id=request.POST['order_id']
        order=Order.objects.get(id=id)
        order.status="Rejected"
        order.save()
        return redirect("order_list")

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

def customer_logout(request):
    response = redirect('customer_login')  # Redirect to the login page after logging out
    
    # Optionally, you can delete a custom cookie
    response.delete_cookie('food_order_email')  # Delete the cookie if you set one earlier
    
    return response

def customer_signup(request):
    next_url = "" 
    otp = ''.join([str(secrets.randbelow(10)) for _ in range(4)])  # Generate a 4-digit OTP

    # Capture 'next' URL from GET parameters
    if request.GET.get("next"):
        next_url = request.GET.get('next')

    # Capture email and password if present in GET parameters
    if request.GET.get("email"):
        email = request.GET.get('email')
    if request.GET.get("info"):
        password = request.GET.get('info')

    if request.method == 'POST':
        # Handle the submitted OTP from the user
        submited_otp = request.POST.get('otp')
        email = request.POST.get('info1')
        password = request.POST.get('info2')

        # Check if the submitted OTP matches the one stored in the session
        stored_otp = request.session.get('otp')  # Retrieve OTP from session

        if stored_otp and submited_otp == stored_otp:
            # OTP is valid, create the customer
            customer = Customer(email=email, password=password)
            customer.save()

            # Redirect to the 'next' page (or home)
            response = redirect(next_url if next_url else 'order_status')
            # Set a cookie with the email (valid for 7 days)
            response.set_cookie('food_order_email', email, max_age=3600*24*7)
            return response
        else:
            # If OTP doesn't match, show an error message
            error_message = "Invalid OTP. Please try again."
            return render(request, 'customer_signup.html', {'next': next_url, 'info1': email, 'info2': password, 'error_message': error_message})

    try:
        # Send OTP email to the customer
        subject = 'OTP for Food Order System'
        message = f'Your OTP is: {otp}'
        recipient_list = [email]  # Send OTP to the email entered
        send_mail(subject, message, 'mahmud0132@gmail.com', recipient_list)

        # Store OTP in session for verification
        request.session['otp'] = otp

    except Exception as e:
        # Handle email sending failure (optional)
        print(f"Error sending OTP: {e}")
        error_message = "Error sending OTP. Please try again later."
        return render(request, 'customer_signup.html', {'next': next_url, 'info1': email, 'info2': password, 'error_message': error_message})

    return render(request, 'customer_signup.html', {'next': next_url, 'info1': email, 'info2': password})

def customer_login(request):
    next_url = "" 
    if request.GET.get("next"):
        next_url=request.GET.get('next')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Customer.objects.filter(email=email, password=password).exists():
            #response = HttpResponse("Login successful")
            #response.set_cookie('food_order_email', email, max_age=60*60*24*7)  # Setting the cookie correctly
             # Get the 'next' URL if provided
                       # Set a cookie (example: 'logged_in' cookie)
            if next_url:
                response = redirect(next_url)  # Redirect to 'home' or another page after login
                
                # Set a cookie (it will expire in 1 hour, for example)
                response.set_cookie('food_order_email', email, max_age=360*60*24*7)
                print("Working______________________________________")
                return response
            else:
                response = redirect('order_status')  # Redirect to 'home' or another page after login
                
                # Set a cookie (it will expire in 1 hour, for example)
                response.set_cookie('food_order_email', email, max_age=360*60*24*7)
                print("Working______________________________________")
                return response                
           # Optionally, redirect to a default view if no 'next' URL is provided
        else:
            print(next_url)
            print("GOing Signup________________________________")
            return redirect(f'/customer_signup/?next={next_url}&email={email}&info={password}')
    return render(request, 'customer_login.html',{'next':next_url})