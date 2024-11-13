from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse  # Correct import
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SymptomLog,Message
from .forms import SymptomLogForm
from django.contrib.auth.decorators import login_required

def home(request):
    # If the user is authenticated, show the home page with website info and home remedies
    if request.user.is_authenticated:
        context = {
            'website_info': "Welcome to Balance Wellness - your partner in period health!",
            'home_remedies': [
                "Drink warm tea, such as chamomile or ginger tea, to relieve cramps.",
                "Use a heating pad on your lower abdomen to soothe pain.",
                "Stay hydrated and consider light exercises like yoga.",
                "Include foods rich in magnesium, like bananas, to reduce cramps."
            ],
        }
        return render(request, 'tracker/home.html', context)
    else:
        # If the user is not authenticated, redirect to login page
        return redirect('login')
def index(request):
    # Render the tracker page (index.html)
    if request.user.is_authenticated:
        return render(request, 'tracker/index.html')
    else:
        return redirect('login')

def get_recommendations(request):
    # Handle AJAX call for symptom recommendations
    symptom = request.GET.get('symptom', '')
    severity = int(request.GET.get('severity', 1))

    if symptom.lower() == "cramps":
        recommendation = "Try heat therapy and rest." if severity > 3 else "Do light stretching exercises."
    elif symptom.lower() == "headache":
        recommendation = "Stay hydrated and avoid screens."
    else:
        recommendation = "General wellness tips: Stay active and maintain a balanced diet."

    return JsonResponse({"recommendation": recommendation})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'tracker/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required  # Ensures the user is logged in before accessing this view
def period_tracker(request):
    return render(request, 'tracker/period_tracker.html')  # Assuming this is the page with the symptom generator


def tracker(request):
    return

@login_required
def profile_view(request):
    user = request.user
    symptom_logs = SymptomLog.objects.filter(user=user).order_by('-date')
    
    if request.method == 'POST':
        form = SymptomLogForm(request.POST)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user = user
            new_log.save()
            return redirect('profile')
    else:
        form = SymptomLogForm()

    context = {
        'form': form,
        'symptom_logs': symptom_logs,
    }
    return render(request, 'profile.html', context)



@login_required
def inbox(request):
    messages = request.user.received_messages.order_by("-created")
    return render(request, "inbox.html", {"messages": messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return render(request, "message_detail.html", {"message": message})

@login_required
def send_message(request):
    if request.method == "POST":
        recipient_id = request.POST["recipient"]
        recipient = get_object_or_404(User, id=recipient_id)
        subject = request.POST["subject"]
        body = request.POST["body"]
        Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
        return redirect("inbox")
    users = User.objects.exclude(id=request.user.id)
    return render(request, "send_message.html", {"users": users})


