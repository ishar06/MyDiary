from django.db import models
from django.contrib.auth.models import User

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Text formatting options
    font_style = models.CharField(max_length=50, choices=FONT_CHOICES, default='Arial')
    font_size = models.CharField(max_length=3, choices=FONT_SIZE_CHOICES, default='16')
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    is_underline = models.BooleanField(default=False)
    is_strikethrough = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Diary Entries'

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
