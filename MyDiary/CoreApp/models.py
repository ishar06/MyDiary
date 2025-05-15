from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class DiaryImage(models.Model):
    image = models.ImageField(upload_to='diary_images/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

class DiaryEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('lonely', 'Lonely'),
        ('depressed', 'Depressed'),
        ('excited', 'Excited'),
        ('peaceful', 'Peaceful'),
    ]

    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('travel', 'Travel'),
        ('health', 'Health'),
        ('others', 'Others'),
    ]

    FONT_CHOICES = [
        ('Arial', 'Arial'),
        ('Times New Roman', 'Times New Roman'),
        ('Courier New', 'Courier New'),
        ('Georgia', 'Georgia'),
        ('Verdana', 'Verdana'),
    ]

    FONT_SIZE_CHOICES = [
        ('12', '12px'),
        ('14', '14px'),
        ('16', '16px'),
        ('18', '18px'),
        ('20', '20px'),
        ('24', '24px'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Text formatting options - simplified
    font_style = models.CharField(max_length=50, choices=FONT_CHOICES, default='Arial')
    font_size = models.CharField(max_length=3, choices=FONT_SIZE_CHOICES, default='16')
    text_color = models.CharField(max_length=7, default='#000000')  # Hex color code
    
    # Legacy fields - kept for compatibility
    is_bold = models.BooleanField(null=True, default=False)
    is_italic = models.BooleanField(null=True, default=False)
    is_underline = models.BooleanField(null=True, default=False)
    is_strikethrough = models.BooleanField(null=True, default=False)

    # Add images field
    images = models.ManyToManyField(DiaryImage, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Diary Entries'

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
