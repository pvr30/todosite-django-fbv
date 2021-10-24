from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request):
    # get the logged in user
    cur_user = request.user
    # print(cur_user.id)
    id = cur_user.id

    tasks = Task.objects.filter(user=id).order_by('-created_date')
    data = {
        'tasks': tasks,
    }
    return render(request, 'todo/home.html', data)


@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        user = request.user
        task = request.POST['task']

        task = Task(user=user, task=task)

        task.save()
        return redirect('home')
    
    # return render(request, 'todo/home.html')


@login_required(login_url='login')
def deleteconfirm(request, id):
    task = get_object_or_404(Task, pk=id)

    task.delete()
    return redirect('home')


@login_required(login_url='login')
def deletetask(request, id):
    # print("work")
    task = get_object_or_404(Task, pk=id)

    data = {
        'task': task
    }
    return render(request, 'todo/delete.html', data)


@login_required(login_url='login')
def edit(request, id):
    task = get_object_or_404(Task, pk=id)

    data = {
        'task': task
    }

    if request.method == 'POST':
        update_task = request.POST['updated_task']
        Task.objects.filter(id=id).update(task=update_task)
        return redirect('home')

    return render(request, 'todo/edit.html', data)


@login_required(login_url='login')
def search(request):
    tasks = Task.objects.order_by("-created_date")

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            tasks = tasks.filter(task__icontains=keyword)
    # print(tasks)
    data = {
        'tasks':tasks,
    }

    return render(request, 'todo/home.html', data)



# authentication

def register(request):
    form = UserCreationForm()

    data = {
        'form':form
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('home')
        else:
            messages.warning(request, 'password do not match')
            return redirect('register')
        
    return render(request, 'account/register.html', data)


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('home')
        else:
            messages.warning(request, 'invalid crendentials')
            return redirect('login')
    return render(request, 'account/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')