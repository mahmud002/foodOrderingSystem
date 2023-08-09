from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from .models import *
from .forms import *
import os
from django.conf import settings
import json
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.
def index(request):
    
    return render(request,'home.html')

##Profile Section
def profile(request):
    if request.user.is_authenticated:
        profile_data = Profile.objects.get(user=request.user)
        order_request=Order.objects.filter(owner=request.user,status="not_taken")
        order_accepted=Order.objects.filter(owner=request.user,status="accepted")
        url="http://127.0.0.1:8000/catalog/"+str(profile_data.user)
        return render(request,'profile.html',{'profile_data':profile_data, 'url':url, 'order':order_request,'order_accepted':order_accepted })
    else:
        return render(request,'login.html')
    
def edit_profile (request):
        if request.user.is_authenticated:

            if request.method=='POST':
                pi=Profile.objects.get(user=request.user)

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

def insert_food(request):
    if request.user.is_authenticated:       
        form=FoodForm()
        pi=Profile.objects.get(user=request.user)
        data = pi.food_list
        title_list=[]
        for i in data:
            title_list.append(i['food_title'])
        if request.method =='POST':
            form=FoodForm(request.POST,request.FILES)
            
            if form.is_valid():
                new_object = {
                    'index':len(data),
                    'food_title': str(form.cleaned_data['food_title']),
                    'food_price': str(form.cleaned_data['food_price']),
                     'food_image' : "home/images/"+str(form.cleaned_data['food_image']).replace(' ','_')
                }
                full_path = os.path.join(settings.MEDIA_ROOT, new_object['food_image'])
                image_file = form.cleaned_data['food_image']
                image_data = image_file.read()
                with open(full_path, 'wb') as f:
                    f.write(image_data)


                
                data.append(new_object)
                pi.food_list = data
                pi.save()
                
                # instance.username=request.user.profile
                # form.save()
               
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
                py_food.index=product_id
                py_food.food_title=food['food_title']
                py_food.food_price=food['food_price']
                py_food.food_image=food['food_image']

                
                form=FoodForm(instance=py_food)
                
                return render(request,'food_edit_form.html',{'form':form})
            else:
                form=FoodForm(request.POST, request.FILES, instance=py_food)
                if form.is_valid():                    
                    food_list=pk.food_list
                    
                    
                    food=food_list[int(form.cleaned_data['index'])]
                    food['food_title']=form.cleaned_data['food_title']
                    food['food_price']=form.cleaned_data['food_price']
                    clear=form.cleaned_data['clear_image_url']

                    print(clear)
                    
                    if clear:
                        food['food_image']=""
                    elif not form.cleaned_data['food_image'] :
                        food['food_image']=food['food_image']
                    
                    else:
                        food['food_image']="home/images/"+str(form.cleaned_data['food_image'])
                        full_path = os.path.join(settings.MEDIA_ROOT, food['food_image'])
                        image_file = form.cleaned_data['food_image']
                        image_data = image_file.read()
                        with open(full_path, 'wb') as f:
                            f.write(image_data)
                    pk.save()
                    
                    # food['food_title']=form.cleaned_data['food_title'],
                    # food['food_price']=form.cleaned_data['food_price'],
                    # food['food_image']=form.cleaned_data['food_image']

                    pk.save()
                
                    # image_data = image_file.read()
                    # print("______XXXXXXXXXXXX_________")
                    # with open(full_path, 'wb') as f:
                    #     f.write(image_data)


                
                    # data[int(py_food.index)]=new_object
                    # pk.food_list = data
                    # pk.save()
    return redirect('profile')


def delete_food(request):
    if request.user.is_authenticated:
        pk=Profile.objects.get(user=request.user)
        product_id=request.POST['product_id']
        food_list=pk.food_list
        food=find_dictionary_by_data(food_list, "food_title", product_id)
        food_list.remove(food)
        pk.food_list=food_list
        pk.save()
    return redirect('profile')

def catalog(request,key):
    user = get_object_or_404(User, username=key)
    food_list=Profile.objects.filter(user=user).values('food_list').first()['food_list']
    return render(request,'catalog.html',{'food_list':food_list,'key':key})


def submit_order(request):
    if request.method == 'POST':
        # Process the submitted data
        cart_items = request.POST.get('cartItems')  # Access the submitted data
        
        data=json.loads(cart_items)
        key=get_object_or_404(User, username=data[0]['key'])
        new_order=Order(owner=key,food_list=data,status="not_taken")
        
        print("___________________________________________")
        new_order.save()
  
        
        return redirect("/")
   
##Login Logout
def login (request):
    if request.method=='POST':
        username1=request.POST['username']
        password1=request.POST['password']
        print(username1)
        user=authenticate(username=username1,password=password1)

        if user is None:
            return redirect('login')            
        else: 
            if Profile.objects.filter(user=user).exists():
                print("Found")
            else:
                new_pro=Profile(user=user)
                new_pro.save()
                
            
            auth.login(request, user)
            return redirect('/')
            
    
    else:    
         return render(request,'login.html')



    return render(request,'login.html')
def logout (request):
    if request.user.is_authenticated:
        auth.logout(request)
        return HttpResponse("You logout successfully")
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
