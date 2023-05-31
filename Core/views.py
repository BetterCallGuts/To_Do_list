from django.shortcuts import render, redirect
from .models import Account, ToDoTask
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from datetime import datetime






@login_required()
def HomePage(request):
    current_user = User.objects.get(username= request.user.username)
    Acc_model = Account.objects.get(user= current_user)
    tasks = ToDoTask.objects.filter(user = Acc_model)
    v = {
        'tasks' : tasks
    }
    
    
    return render(request, 'app/to_do_list.html', v)


@login_required()
def Logout(request):
    auth.logout(request)
    return redirect('core:Login')


def Login(request):
    
    
    if request.user.is_authenticated :
        return redirect('core:HomePage')
        
    else:
        if request.method == 'POST':
            user_name = request.POST['name']
            pasword = request.POST['pass']

            if not user_name:
                messages.info(request, 'Name is empty!')
                return redirect('core:Login')
            if not pasword:
                messages.info(request, "Password is empty!")
                return redirect('core:Login')
            user = auth.authenticate(username=user_name, password=pasword)
            if user is not None:
                auth.login(request, user)
                return redirect('core:HomePage')
            else:
                messages.info(request, 'invalid user name or password!')
                return redirect('core:Login')
        else:
            
            

        
            return render(request, 'app/login.html')
        

def Signup(request):

    if request.user.is_authenticated :
        return redirect('core:HomePage')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['passw']
            passwordconfirm = request.POST['passw2']
            
            if not username:
                messages.info(request, 'user name is empty!!')
                return redirect("core:Signup")
                
            if not password:
                messages.info(request, 'password is empty!!')
                return redirect("core:Signup")

            
            if not passwordconfirm:
                messages.info(request, "confirm password plz!")
                return redirect("core:Signup")
            

            if password == passwordconfirm:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Name is taken!!')
                    return redirect('core:Signup')
                else:
                    user_new = User.objects.create_user(username=username, password=password )
                    user_new.save()
                    
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    user_for_acc_models = User.objects.get(username= username)
                    new_acc_model  =Account.objects.create(user=user_for_acc_models)
                    new_acc_model.save()
                    return redirect('core:HomePage')


            
            else:
                messages.info(request, "Password didn't match!")
                return redirect("core:Signup")
        else:
            return render(request, 'app/sigup.html')


@login_required()
def Add_A_Task(request):
    if  request.method == "POST":
        title = request.POST['ti']
        description = request.POST['description']
        
        if not title :
            messages.info(request, "Card must have title!")
            return redirect('core:AddATask')
        if not description :
            messages.info(request, "Card must have description!")
            return redirect('core:AddATask')
        
        current_user = User.objects.get(username= request.user.username)
        Acc_model = Account.objects.get(user=current_user)

        ToDoTask.objects.create(user=Acc_model, Title=title, description=description, Created_at=datetime.now())

        return redirect('core:HomePage')
    
    else:
        return render(request, 'app/addtask.html')


@login_required()
def Logout(request):
    
    logout(request)
    messages.success(request, 'You succefully loged out!')

    return redirect('core:Signup'   )

def delete(request, pk):
    task = ToDoTask.objects.filter(pk=pk)
    task.delete()
    return redirect('core:HomePage')


def Edit(request, pk):
    current_user =User.objects.get(username=request.user.username )
    Acc_model = Account.objects.get(user = current_user)
    task = ToDoTask.objects.get(user=Acc_model)
    Title = task.Title
    description = task.description
    if request.method == 'POST':
        form_title = request.POST['ti']
        form_description = request.POST["description"]
        task.Title = form_title
        task.description = form_description
        task.Created_at = datetime.now()
        task.save()

        return redirect('core:HomePage')
    
    else:
        current_user =User.objects.get(username=request.user.username )
        Acc_model = Account.objects.get(user = current_user)
        task = ToDoTask.objects.get(user=Acc_model)
        Title = task.Title
        description = task.description
        v = {
            'Title' : Title,
            'desc'  : description,
        }
        return render(request, 'app/edit.html', v)
