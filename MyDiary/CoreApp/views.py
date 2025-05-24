from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q, Count
from django.http import JsonResponse
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DiaryEntry, UserProfile, DiaryImage
from .forms import CustomUserCreationForm, DiaryEntryForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    mood_filter = request.GET.get('mood', '')
    category_filter = request.GET.get('category', '')
    entries = DiaryEntry.objects.filter(user=request.user)
    
    if mood_filter:
        entries = entries.filter(mood=mood_filter)
    
    if category_filter and category_filter != 'all':
        entries = entries.filter(category=category_filter)
    
    entries = entries.prefetch_related('images').order_by('-created_at')[:10]  # Only get latest 10 entries
    context = {
        'entries': entries,
        'moods': DiaryEntry.MOOD_CHOICES,
        'categories': DiaryEntry.CATEGORY_CHOICES,
        'current_mood': mood_filter,
        'current_category': category_filter
    }
    return render(request, 'home.html', context)

@login_required
def new_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            captions = request.POST.get('image_captions', '').split('\n')
            captions = [cap.strip() for cap in captions if cap.strip()]
            
            for i, image in enumerate(images[:3]):  # Limit to 3 images
                caption = captions[i] if i < len(captions) else ''
                diary_image = DiaryImage.objects.create(
                    image=image,
                    caption=caption
                )
                entry.images.add(diary_image)
            
            messages.success(request, 'Diary entry created successfully!')
            return redirect('home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/new_entry.html', {'form': form})

@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('images')
            captions = request.POST.get('image_captions', '').split('\n')
            captions = [cap.strip() for cap in captions if cap.strip()]
            
            current_count = entry.images.count()
            remaining_slots = 3 - current_count
            
            for i, image in enumerate(images[:remaining_slots]):
                caption = captions[i] if i < len(captions) else ''
                diary_image = DiaryImage.objects.create(
                    image=image,
                    caption=caption
                )
                entry.images.add(diary_image)
            
            messages.success(request, 'Diary entry updated successfully!')
            return redirect('home')
    else:
        form = DiaryEntryForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'entry_images': entry.images.all()
    }
    return render(request, 'diary/edit_entry.html', context)

@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Diary entry deleted successfully!')
    return redirect('home')

@login_required
def delete_image(request, entry_pk, image_pk):
    entry = get_object_or_404(DiaryEntry, pk=entry_pk, user=request.user)
    image = get_object_or_404(DiaryImage, pk=image_pk)
    
    if request.method == 'POST':
        if image in entry.images.all():
            entry.images.remove(image)
            image.delete()  # This will also delete the file
            messages.success(request, 'Image deleted successfully!')
        
    return redirect('edit_entry', pk=entry_pk)

@login_required
def search_entries(request):
    query = request.GET.get('q', '')
    mood_filter = request.GET.get('mood', '')
    category_filter = request.GET.get('category', '')
    
    entries = DiaryEntry.objects.filter(user=request.user)
    
    if query:
        entries = entries.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    if mood_filter:
        entries = entries.filter(mood=mood_filter)
    
    if category_filter and category_filter != 'all':
        entries = entries.filter(category=category_filter)
    
    entries = entries.prefetch_related('images').order_by('-created_at')
    
    context = {
        'entries': entries,
        'query': query,
        'moods': DiaryEntry.MOOD_CHOICES,
        'categories': DiaryEntry.CATEGORY_CHOICES,
        'current_mood': mood_filter,
        'current_category': category_filter
    }
    return render(request, 'diary/search_results.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def get_stats(request):
    # Get user's entries
    entries = DiaryEntry.objects.filter(user=request.user)
    
    # Calculate total entries
    total_entries = entries.count()
    
    # Get mood distribution
    mood_stats = entries.values('mood').annotate(count=Count('id'))
    mood_distribution = {item['mood']: item['count'] for item in mood_stats}
    
    # Get category distribution
    category_stats = entries.values('category').annotate(count=Count('id'))
    category_distribution = {item['category']: item['count'] for item in category_stats}
    
    # Get entries per day (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_entries = (
        entries.filter(created_at__gte=thirty_days_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    timeline_data = {
        'dates': [item['date'].strftime('%Y-%m-%d') for item in daily_entries],
        'counts': [item['count'] for item in daily_entries]
    }
    
    # Calculate streak
    current_streak = 0
    longest_streak = 0
    last_date = None
    
    daily_entries = entries.annotate(date=TruncDate('created_at')).values('date').distinct().order_by('-date')
    
    for entry in daily_entries:
        current_date = entry['date']
        if last_date is None:
            current_streak = 1
        elif (last_date - current_date).days == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
        last_date = current_date
    
    longest_streak = max(longest_streak, current_streak)
    
    # Get monthly trend
    monthly_stats = (
        entries.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    monthly_trend = {
        'months': [item['month'].strftime('%Y-%m') for item in monthly_stats],
        'counts': [item['count'] for item in monthly_stats]
    }
    
    # Calculate average entries per day
    if total_entries > 0:
        first_entry = entries.order_by('created_at').first()
        days_since_first = (timezone.now().date() - first_entry.created_at.date()).days + 1
        avg_entries_per_day = round(total_entries / days_since_first, 2)
    else:
        avg_entries_per_day = 0
    
    stats = {
        'total_entries': total_entries,
        'mood_distribution': mood_distribution,
        'category_distribution': category_distribution,
        'timeline_data': timeline_data,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'monthly_trend': monthly_trend,
        'avg_entries_per_day': avg_entries_per_day
    }
    
    return JsonResponse(stats)
