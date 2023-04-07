from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code, resettoken
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from .utils import SendResetLink, generateToken
from django.conf import settings
from django.contrib.auth.hashers import make_password
import os
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key from the environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# this can be improved and with CHOICEFIELD


@csrf_exempt
def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'markup',
                 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r',
                 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']
    actions = ['Fix', 'Suggest', 'Explain', 'Write document']
    if request.method == "POST":
        code = request.POST.get('code')
        lang = request.POST.get('lang')
        action = request.POST.get('action')
        # checking if user types anything on the text box
        if not code:
            messages.success(
                request, "Please speak or add message....")
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'message': code, 'lang': lang, 'action': action, 'action_list': actions})
        # Check to make sure they picked a lang
        elif lang == "Select Programming Language":
            messages.success(
                request, "Please pick a programming language...")
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'message': code, 'lang': lang, 'action': action, 'action_list': actions})
        elif action == "Select action":
            messages.success(request, "Please pick an action...")
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'message': code, 'lang': lang, 'action': action, 'action_list': actions})
        else:
            openai.api_key = OPENAI_API_KEY
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                response = (response["choices"][0]["text"])
                record = Code(question=code, code_answer=response,
                              language=lang, user=request.user)
                record.save()
                return render(request, 'home.html', {'lang_list': lang_list, 'response': response, 'lang': lang, 'action': action, 'action_list': actions})

            except Exception as e:
                print(e)
                return render(request, 'home.html', {'lang_list': lang_list, 'response': e, 'lang': lang, 'action': action, 'action_list': actions})

    return render(request, 'home.html', {'lang_list': lang_list, 'action_list': actions})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Error Logging In. Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password, email=email)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    return render(request, 'register.html', {"form": form})


def past(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        messages.success(request, "You Must Be Logged In To View This Page")
        return redirect('home')


def delete_past(request, Past_id):
    past = Code.objects.get(pk=Past_id)
    if request.user != past.user:
        messages.success(request, "You are not allowed to delete...")
        return redirect('past')
    past.delete()
    messages.success(request, "Deleted Successfully...")
    return redirect('past')

def password_reset_verified(request, id):
    valid = False
    validtoken = resettoken.objects.filter(token=id)
    if validtoken:
        valid = True
    if request.method == "POST":
        validtoken = resettoken.objects.filter(token=id)
        if validtoken:
            validtoken = resettoken.objects.filter(token=id)[0]
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                messages.success(
                    request, "Passwords do not match. Please try again.")
                return render(request, 'newpassword.html', {"valid": valid})
            user = User.objects.get(user=validtoken)
            user.password = make_password(password)
            user.save()
            validtoken.token = ''
            validtoken.save()
            messages.success(request, 'Password Change Successfully...')
            return redirect('login')
    return render(request, 'newpassword.html', {"valid": valid})

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        currentuser = User.objects.filter(email=email)
        if currentuser:
            currentuser = User.objects.filter(email=email)[0]
            try:
                usertoken = resettoken.objects.get(user=currentuser)
            except:
                usertoken = resettoken.objects.create(user=currentuser)
            token = generateToken()
            usertoken.token = token
            usertoken.save()
            user = currentuser.username
            subject = "Codegen password reset instructions"
            link = settings.DOMAIN + "/forgot_password/" + token
            body = f"Hi {user}, \nAs you have requested for reset password instructions, here they are, please follow the URL: \n{link}\nAlternatively, open the url in your browser.\n"
            if SendResetLink(subject, body, email):
                messages.success(request, "Reset Link Send Successfully...")

        return render(request, 'passwordreset.html', {"page": 'success'})
    return render(request, 'passwordreset.html')