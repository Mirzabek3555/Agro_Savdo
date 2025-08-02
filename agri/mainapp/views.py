from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def index(request):
    return render(request, 'home.html')


def crop_type_list(request):
    crop_types = models.CropType.objects.all()
    return render(request, 'crop_type_list.html', {'crop_types': crop_types})


def crop_type_list(request):
    
    crop_types = models.CropType.objects.prefetch_related('images').all()
    return render(request, 'crop_type_list.html', {'crop_types': crop_types})


def crop_type_detail(request, crop_id):
    """Displays details of a specific crop type with its images."""
    crop_type = get_object_or_404(models.CropType, id=crop_id)
    images = models.CropImage.objects.filter(crop_type=crop_type)  # Fetch related images
    return render(request, 'crop_type_detail.html', {'crop_type': crop_type, 'images': images})


def farmer_crop_list(request):
    """Displays all crops posted by farmers."""
    farmer_crops = models.FarmerCrop.objects.select_related('crop_type', 'farmer').all()
    return render(request, 'farmer_crop_list.html', {'farmer_crops': farmer_crops})


def farmer_crop_detail(request, crop_id):
    """Displays details of a specific crop being sold by a farmer."""
    farmer_crop = get_object_or_404(models.FarmerCrop.objects.select_related('crop_type', 'farmer'), id=crop_id)
    return render(request, 'farmer_crop_detail.html', {'farmer_crop': farmer_crop})


def crops_by_type(request, crop_type_id):
    """Displays all crops posted by farmers for a specific crop type."""
    crop_type = get_object_or_404(models.CropType, id=crop_type_id)
    farmer_crops = models.FarmerCrop.objects.filter(crop_type=crop_type).select_related('farmer')

    return render(request, 'crops_by_type.html', {
        'crop_type': crop_type,
        'farmer_crops': farmer_crops
    })


def market_price(request):
    return render(request, 'market_price.html')


def post_crops(request):
    return render(request, 'post_crops.html')


def crop_calendar_view(request):
    """Render the calendar page."""
    return render(request, 'crop_calendar.html')

def crop_events(request):
    """Return crop planting & harvesting periods as JSON for FullCalendar.js"""
    crops = models.CropCalendar.objects.all()
    events = []

    for crop in crops:
        events.append({
            'title': f"Plant {crop.crop_name}",
            'start': crop.planting_start.strftime('%Y-%m-%d'),
            'end': crop.planting_end.strftime('%Y-%m-%d'),
            'color': 'green'
        })
        events.append({
            'title': f"Harvest {crop.crop_name}",
            'start': crop.harvesting_start.strftime('%Y-%m-%d'),
            'end': crop.harvesting_end.strftime('%Y-%m-%d'),
            'color': 'orange'
        })

    return JsonResponse(events, safe=False)


@login_required
def submit_crop_entry(request):
    if request.method == "POST":
        crop_ids = request.POST.getlist("crop_type[]")
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")

        for crop_id, quantity, price in zip(crop_ids, quantities, prices):
            if quantity and price:  # Ensure valid input
                crop_type = models.CropType.objects.get(id=crop_id)
                models.FarmerCrop.objects.create(
                    farmer=request.user,
                    crop_type=crop_type,
                    quantity_kg=quantity,
                    price_per_kg=price,
                    location="Unknown",  # You can update this dynamically
                    available_from="2025-02-01",  # Add logic to handle actual dates
                    available_until="2025-12-31",
                )

        messages.success(request, "Crops submitted successfully!")
        return redirect("crop_type_list") 

    return render(request, 'post_crops.html', {'crop_types': models.CropType.objects.prefetch_related('images').all()}) 


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful!")
            return redirect("crop_type_list")
    else:
        form = UserCreationForm()
    
    return render(request, "users/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("crop_type_list")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
