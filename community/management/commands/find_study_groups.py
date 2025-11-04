import networkx as nx
from django.core.management.base import BaseCommand
from users.models import User
from community.models import SuggestedStudyGroup
from collections import defaultdict

class Command(BaseCommand):
    help = 'Finds and creates study groups based on university and course.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting study group analysis...'))

        # Clear out old suggestions
        SuggestedStudyGroup.objects.all().delete()

        # 1. Get all users who have a university and course
        users = User.objects.filter(
            university__isnull=False,
            course__isnull=False
        ).exclude(university__exact='').exclude(course__exact='')

        if not users.exists():
            self.stdout.write(self.style.WARNING('No users with university and course data. Aborting.'))
            return

        # 2. Group users by (university, course)
        groups = defaultdict(list)
        for user in users:
            key = (user.university, user.course)
            groups[key].append(user)

        self.stdout.write(f'Found {len(groups)} potential groups.')

        # 3. Create SuggestedStudyGroup objects
        created_count = 0
        for (university, course), members in groups.items():
            # Only create groups with 2 or more people
            if len(members) >= 2:
                # Create the new group object
                group = SuggestedStudyGroup.objects.create(
                    course_name=course,
                    university_name=university
                )
                # Add all members to the group
                group.members.set(members)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} study groups.'))