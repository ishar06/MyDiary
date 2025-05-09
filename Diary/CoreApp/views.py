from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from .models import DiaryEntry
from .forms import CustomUserCreationForm, DiaryEntryForm

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
    entries = DiaryEntry.objects.filter(user=request.user)
    
    if mood_filter:
        entries = entries.filter(mood=mood_filter)
    
    entries = entries.order_by('-created_at')
    context = {
        'entries': entries,
        'moods': DiaryEntry.MOOD_CHOICES,
        'current_mood': mood_filter
    }
    return render(request, 'home.html', context)

@login_required
def new_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Diary entry created successfully!')
            return redirect('home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/new_entry.html', {'form': form})

@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diary entry updated successfully!')
            return redirect('home')
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Diary entry deleted successfully!')
    return redirect('home')

@login_required
def search_entries(request):
    query = request.GET.get('q', '')
    mood_filter = request.GET.get('mood', '')
    
    entries = DiaryEntry.objects.filter(user=request.user)
    
    if query:
        entries = entries.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    if mood_filter:
        entries = entries.filter(mood=mood_filter)
    
    entries = entries.order_by('-created_at')
    
    context = {
        'entries': entries,
        'query': query,
        'moods': DiaryEntry.MOOD_CHOICES,
        'current_mood': mood_filter
    }
    return render(request, 'diary/search_results.html', context)
