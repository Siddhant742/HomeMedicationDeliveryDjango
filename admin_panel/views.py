from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User  # Import User model from account app
from transaction.models import Prescription, Order  # Import Prescription and Order models from transaction app

def index(request):
    print("Rendering index page")
    return render(request, 'backend/index.html')

def login_view(request):
    print("Login view called")
    if request.user.is_authenticated:
        return redirect('backend:index')

    if request.method == "POST":
        print("POST request received")
        username = request.POST.get('username')
        # email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request,  username = username, password=password,)
        print(f"Authenticated user: {user}")

        if user is not None:
            if user.is_superuser or user.is_staff:
                print("User is superuser or staff")
                auth_login(request, user)
                return redirect('backend:index')
            else:
                print("User is not superuser or staff")
                messages.warning(request, 'Invalid credentials or insufficient permissions.')
        else:
            print("Invalid email or password")
            messages.warning(request, "Invalid email or password.")

    return render(request, 'backend/login.html')

@login_required
def userlogout(request):
    print("User logout called")
    auth_logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('backend:login_view')

@login_required
def verify_user_id_images(request):
    print("Verify user ID images called")
    users = User.objects.filter(verification_status='pending')
    if request.method == 'POST':
        print("POST request received for verifying user ID images")
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        print(f"User ID: {user_id}, Action: {action}")
        user = get_object_or_404(User, id=user_id)
        if action == 'approve':
            user.verification_status = 'verified'
        elif action == 'reject':
            user.verification_status = 'rejected'
        user.save()
        messages.success(request, f"User {user.username}'s ID verification status updated.")
        return redirect('backend:verify_user_id_images')
    return render(request, 'backend/verify_user_id_images.html', {'users': users})

@login_required
def verify_prescriptions(request):
    print("Verify prescriptions called")
    prescriptions = Prescription.objects.filter(status='pending')
    if request.method == 'POST':
        print("POST request received for verifying prescriptions")
        prescription_id = request.POST.get('prescription_id')
        action = request.POST.get('action')
        print(f"Prescription ID: {prescription_id}, Action: {action}")
        prescription = get_object_or_404(Prescription, id=prescription_id)
        if action == 'approve':
            prescription.status = 'verified'
        elif action == 'reject':
            prescription.status = 'rejected'
        prescription.save()
        messages.success(request, f"Prescription {prescription.id} status updated.")
        return redirect('backend:verify_prescriptions')
    return render(request, 'backend/verify_prescriptions.html', {'prescriptions': prescriptions})

@login_required
def view_orders(request):
    print("View orders called")
    orders = Order.objects.all()
    return render(request, 'backend/view_orders.html', {'orders': orders})

@login_required
def user_list(request):
    print("User list called")
    users = User.objects.all()
    return render(request, 'backend/user_list.html', {'users': users})

@login_required
def user_order_list(request, user_id):
    print("User order list called")
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user)
    return render(request, 'backend/user_order_list.html', {'orders': orders, 'user': user})