from django.core.management.base import BaseCommand
from CoreApp.models import DiaryEntry
from cryptography.fernet import Fernet
from django.conf import settings

class Command(BaseCommand):
    help = 'Fixes encryption for diary entries'

    def handle(self, *args, **options):
        key = getattr(settings, 'ENCRYPTION_KEY', None)
        if not key:
            self.stdout.write(self.style.ERROR('ENCRYPTION_KEY not set in settings'))
            return

        fernet = Fernet(key)
        entries = DiaryEntry.objects.all()

        for entry in entries:
            try:
                # Try to decrypt the content
                try:
                    # If this succeeds, it's encrypted
                    decrypted = fernet.decrypt(entry.content.encode())
                    # Re-save the entry to trigger the encryption logic
                    entry.content = decrypted.decode()
                    entry.save()
                except:
                    # If it fails, the content isn't encrypted, just save it
                    entry.save()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing entry {entry.id}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS('Successfully fixed all entries'))