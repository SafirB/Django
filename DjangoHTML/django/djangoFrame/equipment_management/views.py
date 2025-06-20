from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Item, Reservation
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Reservation



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('equipment_management:login')  # Redirect to login after account creation
    else:
        form = CustomUserCreationForm()
    return render(request, 'equipment_management/signup.html', {'form': form})

@login_required
def create_reservation(request, item_id):
    # Ensure the item exists and can be reserved
    item = get_object_or_404(Item, item_id=item_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        # Create the reservation
        reservation = Reservation(
            user=request.user,
            item=item,
            date=date,
            time=time,
            status='Pending'  # Status Is pending by Default
        )
        reservation.save()

        # Redirect to product list
        return redirect('equipment_management:product_list')

    # Display Reservation form if not a post request
    return render(request, 'equipment_management/create_reservation.html', {'item': item})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reservation deleted successfully!")
        return redirect('equipment_management:reservation_list')
    else:
        messages.error(request, "Invalid request")
        return redirect('equipment_management:reservation_list')

def reports_view(request):
    # Add Stuff here later
    return render(request, 'equipment_management/reports.html')

def is_admin(user):
    return user.is_staff  # Lets staff members be admins

@login_required # Only admins can see and access the dashboard
@user_passes_test(is_admin)
def dashboard_view(request):
    return render(request, 'equipment_management/dashboard.html')

def reservation_success(request):
    # Display success message
    return HttpResponse('Reservation successful!')

def view_inventory(request):
    items = Item.objects.all()  # Retrieve all items from the database
    return render(request, 'equipment_management/inventory_report.html', {'items': items})

def product_list(request):
    items = Item.objects.all()  # Retrieves all records from the item_item table
    return render(request, 'equipment_management/products.html', {'items': items})

def reservation_list(request):
    # Retrieve all reservations for the logged-in user
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'equipment_management/reservation.html', {'reservations': user_reservations})

# Stuff to manage and change account details
@login_required
def manage_account(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user) # Forms for changing details
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('account_management_success')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    reservations = Reservation.objects.filter(user=request.user, status__in=['approved', 'denied']) # Filters so that only approved or denied requests show up on manage account page

    return render(request, 'equipment_management/manage_account.html', {
        'user_form': user_form,
        'password_form': password_form,
        'reservations': reservations
    })

def equipment_usage_history_view(request):
    # Only gets reservations that have been approved
    approved_reservations = Reservation.objects.filter(status='approved')
    return render(request, 'equipment_management/equipment_usage_history.html', {'reservations': approved_reservations})