from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, UserFileForm
from .models import UserProfile, StudyMaterial,UserFile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'DNAcon/home.html')


def signupuser(request):
    page = "register"
    form = CustomUserCreationForm
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower().strip()
            user.save()

            # Проверяем, существует ли профиль пользователя, и создаем его, если нет
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.save()
            group = form.cleaned_data['group']
            user_profile.Project_type = form.cleaned_data['Project_type']

            # if user_profile.group == '- - класс' or user_profile.Project_type == '- -':
            #     user_profile.delete()
            #     messages.error(request, 'Пожалуйста, выберите действительную группу и тип проекта!')
            #     return redirect('signup')

            user_profile.save()

            # Пример: добавление пользователя в группу
            if group == '5-6 класс':
                user.groups.add(Group.objects.get(name='5-6 класс'))
            elif group == '7-8 класс':
                user.groups.add(Group.objects.get(name='7-8 класс'))
            elif group == '9-11 класс':
                user.groups.add(Group.objects.get(name='9-11 класс'))

            messages.success(request, "Учетная запись пользователя была создана!")
            login(request, user)
            return redirect('current')
        else:
            messages.error(request, 'Произошла ошибка во время регистрации!')

    context = {'page': page, 'form': form}
    return render(request, 'DNAcon/signupuser.html', context)


def loginuser(request):
    if request.method == "GET":
        return render(request,'DNAcon/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'DNAcon/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа!'})
        else:
            login(request,user)
            return redirect('current')


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@login_required
def currenttasks(request):

    materials = StudyMaterial.objects.all()

    return render(request, 'DNAcon/currenttasks.html', {'materials': materials})



@login_required
def user_files(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()
            form = UserFileForm()

    else:
        form = UserFileForm()

    user_files = UserFile.objects.filter(user=request.user)
    return render(request, 'DNAcon/user_files.html', {'form': form, 'user_files': user_files})



@login_required
def delete_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id)

    if user_file.user == request.user:
        user_file.delete()

    return redirect('user_files')
