# core/management/commands/create_test_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

"""
Run this in project root:

python manage.py create_test_user
"""

class Command(BaseCommand):
    help = "Create a test user"

    def handle(self, *args, **kwargs):
        username = "testuser"
        password = "mypassword123"
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
        else:
            self.stdout.write(f"User {username} already exists")
