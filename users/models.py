from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import uuid
from django.core.files.storage import default_storage as storage
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from friendship.models import Friend, FriendshipRequest

YEAR_CHOICES = (
			('1st year', '1st year'),
			('2nd year', '2nd year'),
			('3rd year', '3rd year'),
			('4th year', '4th year'),
		)
MAJOR_CHOICES = (
			('African American & African Studies', 'African American & African Studies'),
			('American Studies', 'American Studies'),
			('Anthropology', 'Anthropology'),
			('Art History', 'Art History'),
			('Art, Studio', 'Art, Studio'),
			('Astronomy', 'Astronomy'),
			('Astronomy-Physics', 'Astronomy-Physics'),
			('Biology', 'Biology'),
			('Chemistry', 'Chemistry'),
			('Chinese Language & Literature', 'Chinese Language & Literature'),
			('Classics', 'Classics'),
			('Cognitive Science', 'Cognitive Science'),
			('Comparative Literature', 'Comparative Literature'),
			('Computer Science', 'Computer Science'),
			('Drama', 'Drama'),
			('East Asian Studies', 'East Asian Studies'),
			('Economics', 'Economics'),
			('English', 'English'),
			('Environmental Sciences', 'Environmental Sciences'),
			('Environmental Thought & Practice', 'Environmental Thought & Practice'),
			('German', 'German'),
			('Global Studies', 'Global Studies'),
			('History', 'History'),
			('Human Biology', 'Human Biology'),
			('Italian', 'Italian'),
			('Japanese Language & Literature', 'Japanese Language & Literature'),
			('Jewish Studies', 'Jewish Studies'),
			('Latin American Studies', 'Latin American Studies'),
			('Linguistics', 'Linguistics'),
			('Mathematics', 'Mathematics'),
			('Media Studies', 'Media Studies'),
			('Medieval Studies', 'Medieval Studies'),
			('Middle Eastern and South Asian Languages and Cultures', 'Middle Eastern and South Asian Languages and Cultures'),
			('Music', 'Music'),
			('Neuroscience', 'Neuroscience'),
			('Philosophy', 'Philosophy'),
			('Physics', 'Physics'),
			('Political and Social Thought', 'Political and Social Thought'),
			('Political Philosophy, Policy, and Law', 'Political Philosophy, Policy, and Law'),
			('Politics', 'Politics'),
			('Psychology', 'Psychology'),
			('Religious Studies', 'Religious Studies'),
			('Slavic Languages and Literatures', 'Slavic Languages and Literatures'),
			('Sociology', 'Sociology'),
			('South Asian Studies', 'South Asian Studies'),
			('Spanish', 'Spanish'),
			('Statistics', 'Statistics'),
			('Teacher Education', 'Teacher Education'),
			('Women, Gender, and Sexuality', 'Women, Gender, and Sexuality'),
			('Aerospace Engineering', 'Aerospace Engineering'),
			('Biomedical Engineering', 'Biomedical Engineering'),
			('Chemical Engineering', 'Chemical Engineering'),
			('Civil Engineering', 'Civil Engineering'),
			('Computer Engineering', 'Computer Engineering'),
			('Computer Science', 'Computer Science'),
			('Electrical Engineering', 'Electrical Engineering'),
			('Engineering Science', 'Engineering Science'),
			('Mechanical Engineering', 'Mechanical Engineering'),
			('Systems Engineering', 'Systems Engineering'),
			('Accounting', 'Accounting'),
			('Finance', 'Finance'),
			('Information Technology', 'Information Technology'),
			('Management', 'Management'),
			('Marketing', 'Marketing'),
			('Architectual History', 'Architectural History'),
			('Architecture', 'Architecture'),
			('Urban & Environmental Planning', 'Urban & Environmental Planning'),
			('Bachelor of Science in Nursing (BSN)', 'Bachelor of Science in Nursing (BSN)'),
			('RN to BSN', 'RN to BSN'),
			('B.A. in Public Policy and Leadership', 'B.A. in Public Policy and Leadership'),
			('Accelerated B.A./Master of Public Policy (MPP) Program', 'Accelerated B.A./Master of Public Policy (MPP) Program'),
			('Kinesiology', 'Kinesiology'),
			('Speech Communications Disorders Major', 'Speech Communications Disorders Major'),
			('Youth & Social Innovation Major', 'Youth & Social Innovation Major'),
			('B.S./M.S. in Teaching', 'B.S./M.S. in Teaching'),
		)
MINOR_CHOICES = MAJOR_CHOICES


class MatchingHistory(models.Model):
  from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matching_requests_sent')
  to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matching_requests_received')
  created = models.DateTimeField(default=timezone.now)
  finished = models.BooleanField(default=False)
  reviewed = models.BooleanField(default=False)
  rating = models.IntegerField(default=1)
  comment = models.TextField(max_length=500, blank=True)
  display_name = models.CharField(max_length=30, default="Anonymous User")
  title = models.CharField(max_length=50, default="Match Request")
  reason = models.TextField(max_length = 300, blank=True)

class MatchRequest(models.Model):
	friend_request = models.OneToOneField(FriendshipRequest, on_delete=models.CASCADE)
	title = models.CharField(max_length=50, default="Match Request")
	reason = models.TextField(max_length = 300, blank=True)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	year = models.CharField(max_length=255, choices=YEAR_CHOICES)
	major = models.CharField(max_length=255, choices=MAJOR_CHOICES)
	major_two = models.CharField(max_length=255, choices=MAJOR_CHOICES, blank=True)
	minor = models.CharField(max_length=255, choices=MINOR_CHOICES, blank=True)
	picture = models.ImageField(upload_to="msn/image/",blank=True)
	avatar = models.ImageField(upload_to="msn/image/avatar/",blank=True)
	online = models.IntegerField(default = 0)

	def save(self, *args, **kwargs):
		# delete old file when replacing by updating the file
		try:
			this = Profile.objects.get(pk=self.pk)
			if this.picture != self.picture:
				this.picture.delete(save=False)
			if self.picture and this.picture != self.picture:
				self.picture = self.compressImage(self.picture, False, 0, 0, 70)
				self.avatar = self.compressImage(self.picture, True, 100, 100, 99)
		except: pass # when new photo then we do nothing, normal case
		super(Profile, self).save(*args, **kwargs)


	def compressImage(self,uploadedImage, resize_bool, w, h, quality):
		imageTemporary = Image.open(uploadedImage)
		outputIoStream = BytesIO()
		if resize_bool:
			imageTemporary = imageTemporary.resize((w,h))
		print("debug picture format:",imageTemporary.format)
		if imageTemporary.format == "PNG":
			imageTemporary = imageTemporary.convert("RGB")
		imageTemporary.save(outputIoStream , format='JPEG', quality=quality)
		outputIoStream.seek(0)
		uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % str(uuid.uuid4()), 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    this = instance
    if this.picture:
    	this.picture.delete(save=False)

@receiver(post_save, sender=FriendshipRequest)
def create_match_request(sender, instance, created, **kwargs):
	if created:
		MatchRequest.objects.create(friend_request=instance)

@receiver(post_save, sender=FriendshipRequest)
def save_match_request(sender, instance, **kwargs):
	instance.matchrequest.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

