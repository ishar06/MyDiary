from django.core.management.base import BaseCommand
from CoreApp.models import DiaryEntry
from cryptography.fernet import Fernet
from django.conf import settings

class Command(BaseCommand):
    help = 'Fixes encryption for existing diary entries'

    def handle(self, *args, **options):
        if not settings.ENCRYPTION_KEY:
            self.stdout.write(self.style.ERROR('ENCRYPTION_KEY not set in settings'))
            return

        fernet = Fernet(settings.ENCRYPTION_KEY)
        entries = DiaryEntry.objects.all()
        fixed_count = 0

        for entry in entries:
            try:
                # Try to decrypt the content first
                try:
                    decrypted_content = fernet.decrypt(entry.content.encode()).decode()
                    # If successful, it's already encrypted, leave it
                    continue
                except:
                    # If decryption fails, it's not encrypted yet
                    # Encrypt the current content
                    encrypted_content = fernet.encrypt(entry.content.encode()).decode()
                    DiaryEntry.objects.filter(id=entry.id).update(content=encrypted_content)
                    fixed_count += 1

                # Do the same for title
                try:
                    decrypted_title = fernet.decrypt(entry.title.encode()).decode()
                except:
                    encrypted_title = fernet.encrypt(entry.title.encode()).decode()
                    DiaryEntry.objects.filter(id=entry.id).update(title=encrypted_title)
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing entry {entry.id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully fixed {fixed_count} entries'))