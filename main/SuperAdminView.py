from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from main.models import CustomUser, SaccoAdmin, Saccos
from .forms import AddMembersForm


# Beginning of the home template
def admin_home(request):
    all_sacco_admin_count = SaccoAdmin.objects.all().count()
    saccos_count = Saccos.objects.all().count()
    context = {
        "all_sacco_admin_count": all_sacco_admin_count,
        "saccos_count": saccos_count,
    }
    return render(request, "superadmin_temp/home_content.html", context)

# End of the home template



# Add sacco_admin
def add_sacco_admin(request):
    return render(request, "superadmin_temp/add_sacco_admin.html")


def add_sacco_admin_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_sacco_admin')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.SaccoAdmins.address = address
            user.save()
            messages.success(request, "Sacco Admin Added Successfully!")
            return redirect('add_sacco_admin')
        except:
            # Error Here
            messages.success(request, "Sacco Admin Added Successfully!")
            return redirect('add_sacco_admin')


def manage_sacco_admin(request):
    sacco_admn = SaccoAdmin.objects.all()
    context = {
        "staffs": sacco_admn
    }
    return render(request, "superadmin_temp/manage_sacco_admin.html", context)


def edit_sacco_admin(request, sacco_admin_id):
    sacco_admn = SaccoAdmin.objects.get(admin=sacco_admin_id)

    context = {
        "staff": sacco_admn,
        "id": sacco_admin_id
    }
    return render(request, "superadmin_temp/edit_sacco_admin.html", context)


def edit_sacco_admin_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sacco_admn = request.POST.get('sacco_admin_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into SaccoAdmin Model
            saccoAdmin_model = SaccoAdmin.objects.get(admin=id)
            saccoAdmin_model.address = address
            saccoAdmin_model.save()

            messages.success(request, "Sacco Admin Updated Successfully.")
            return redirect('/edit_sacco_admin/'+id)

        except:
            messages.error(request, "Failed to Update Sacco Admin.")
            return redirect('/edit_sacco_admin/'+id)


def delete_sacco_admin(request, sacco_admin_id):
    sacco_admin = SaccoAdmin.objects.get(admin=sacco_admin_id)
    try:
        sacco_admin.delete()
        messages.success(request, "Sacco Admin Deleted Successfully.")
        return redirect('manage_sacco_admin')
    except:
        messages.error(request, "Failed to Delete Sacco Admin.")
        return redirect('manage_sacco_admin')


# Add Members
def add_member(request):
    form = AddMembersForm()
    context = {
        "form": form
    }
    return render(request, 'superadmin_temp/add_member.html', context)


def add_member_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_member')
    else:
        form = AddMembersForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            sacco_id = form.cleaned_data['sacco_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.members.address = address

                sacco_obj = Saccos.objects.get(id=sacco_id)
                user.members.sacco_id = sacco_obj

                user.members.gender = gender
                user.members.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Member Added Successfully!")
                return redirect('add_member')
            except:
                messages.error(request, "Failed to Add Member!")
                return redirect('add_member')
        else:
            return redirect('add_member')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def superadmin_profile(request):
    user = CustomUser.objects.get(pk=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'superadmin_temp/superadmin_profile.html', context)


def superadmin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('superadmin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(pk=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            # if password != None and password != "":
            # customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('superadmin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('superadmin_profile')


# Beginning of Add Saccos
def add_sacco(request):
    return render(request, "superadmin_temp/add_sacco.html")


def add_sacco_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_sacco')
    else:
        sacco = request.POST.get('sacco')
        try:
            sacco_model = Saccos(sacco_name=sacco)
            sacco_model.save()
            messages.success(request, "Sacco Added Successfully!")
            return redirect('add_sacco')
        except:
            messages.error(request, "Failed to Add Sacco!")
            return redirect('add_sacco')

# End of Add Saccos


# Beginning of Manage Saccos
def manage_saccos(request):
    saccos = Saccos.objects.all()
    context = {
        "courses": saccos
    }
    return render(request, 'superadmin_temp/manage_saccos.html', context)


def manage_members(request):
    return render(request, 'superadmin_temp/manage_members.html')


def edit_sacco(request, course_id):
    saccos = Saccos.objects.get(id=id)
    context = {
        "course": saccos,
        "id": id
    }
    return render(request, 'superadmin_temp/edit_sacco.html', context)

# End of Manage Saccos


def edit_sacco_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        sacco_id = request.POST.get('sacco_id')
        sacco_name = request.POST.get('saccos')

        try:
            saccos = Saccos.objects.get(id=sacco_id)
            saccos.sacco_name = sacco_name
            saccos.save()

            messages.success(request, "Sacco Updated Successfully.")
            return redirect('/edit_sacco/'+sacco_id)

        except:
            messages.error(request, "Failed to Update Sacco.")
            return redirect('/edit_sacco/'+sacco_id)


def delete_sacco(request, course_id):
    saccos = Saccos.objects.get(id=course_id)
    try:
        saccos.delete()
        messages.success(request, "Sacco Deleted Successfully.")
        return redirect('manage_sacco')
    except:
        messages.error(request, "Failed to Delete Sacco.")
        return redirect('manage_sacco')
