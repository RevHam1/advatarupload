from re import A
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages
import bcrypt
import os
# from django.core.files.storage import FileSystemStorage, FileSystemStorage

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        return redirect('/load_image')
    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            user = user[0]      
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/load_image')
        messages.error(request, "Email or password is incorrect")
    return redirect('/')

def load_image(request):
    # context = {}
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_images': Profile.objects.all()
    }
    return render(request, "images.html", context)

def survey(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.success(request, "Choose a File to Upload Image")
            return redirect('/load_image')

        uploaded_file = Profile.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            profile_image = request.FILES['user_img'],
        )
    # return redirect('/result')
    return redirect('/load_image')

def edit_img(request, img_id):
    img = Profile.objects.get(id=img_id)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(img.profile_image) > 0:
                os.remove(img.profile_image.path)
            img.profile_image = request.FILES['user_img']
        img.save()
        messages.success(request, "Profile Image Succefully Updated")
        return redirect('/load_image')

    context = {'img':img}
    return render(request, "edit.html", context)

# def reset_img(request, img_id):
#     img = Profile.objects.get(id=img_id)

#     if len(img.profile_image) > 0:
#         os.remove(img.profile_image.path)

#     return redirect('/load_image')


def delete_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=user_id)

    if len(user.profile.profile_image) > 0:
        os.remove(user.profile.profile_image.path)

    user.delete()
    messages.success(request, "User and Profile Image Succefully Deleted")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

# def result(request):
#     context = {
#         'current_user': User.objects.get(id=request.session['user_id']),
#         'all_images': Profile.objects.all()
#     }
#     return render(request, 'result.html', context)


        
        # uploaded_file = request.FILES['user_img']
        # fs = FileSystemStorage()
        # name = fs.save(uploaded_file.name, uploaded_file)
        # context['url'] = fs.url(name)

        # print(uploaded_file.name)
        # print(uploaded_file.size)
    # return render(request, "images.html", context)

# def user_image(request, user_id):
#     if request.method == 'POST':
#         user_obj = User.objects.get(id=user_id)
#         user_image_obj = UserImage.objects.get(id=user_id)
#         user_img = FileSystemStorage()
