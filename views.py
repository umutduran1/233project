from django.shortcuts import render,redirect
from .forms import UpdateProfileForm2,LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from post.models import Post


def loginView(request):
    if request.user.is_authenticated == False:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        return render(request, "user/form.html", {"form": form,'title':'Giriş Yap',})



def logoutView(request):
    
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def SendMail(subject,content,email):
    msg = EmailMessage(subject,content,EMAIL_HOST_USER, [email])
    msg.send()

def registerView(request):
        
    if request.user.is_authenticated == False:

        emailError = False
        form = RegisterForm(request.POST or None,request.FILES or None)

        if form.is_valid():

            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user.set_password(password)

            email_data = User.objects.filter(email=email)
            if len(email_data) == 0:

                user.save()
                new_user = authenticate(username=user.username, password=password)
                login(request, new_user)
                return redirect('home')
                
            else:
                emailError = True
        context = {
            'form':form,
            'title':'Kayıt Ol',
            'emailError':emailError,
        }
        return render(request, "user/form.html",context)



def myBlogView(request):

    if request.user.is_authenticated:

        posts = Post.objects.filter(user=request.user)
        posts_value = len(posts)

        for x in posts:
            name = 'btn'+str(x.id)

            if name in request.POST:
                item = Post.objects.get(user=request.user,id=x.id)
                item.delete()
                return redirect('myblog')

        context = {
            'posts':posts,
            'posts_value':posts_value,
        }

        return render(request,'user/myblog.html',context)