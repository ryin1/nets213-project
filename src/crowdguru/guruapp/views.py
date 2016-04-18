from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from .models import User

from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):
    # form = UserCreationForm()
    # context = {'title': title, 'form': form}
    return render(request, 'registration/registration_form.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email=None, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            # username exists
            print 'username already exists'
            return render(request, 'registration/registration_form.html', {'error': 'Username exists'})
    else:
        return render(request, 'registration/registration_form.html')



def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        # password is verified
        login(request, user)
        return HttpResponse('Logged in: {}'.format(user.username))
    else:
        context = {'error': 'Incorrect login information.'}
        return render(request, 'registration/registration_form.html', context)


def home(request):
    print 'is_authenticated:', request.user.is_authenticated()
    print 'username:', request.user.username
    return render(request, 'home.html')

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(request, '/accounts/register/complete')

#     else:
#         form = UserCreationForm()
#     token = {}
#     token.update(csrf(request))
#     token['form'] = form

#     return render_to_response('registration/registration_form.html', token)


# def registration_complete(request):
#     return render_to_response('registration/registration_complete.html')

