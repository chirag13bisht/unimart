from django.db import models
from users.models import User

class SuggestedStudyGroup(models.Model):
    # The course this group is for
    course_name = models.CharField(max_length=100)

    # The university this group is at
    university_name = models.CharField(max_length=100)

    # The members of this suggested group
    members = models.ManyToManyField(User, related_name="study_groups")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.university_name} - {self.course_name} Group"