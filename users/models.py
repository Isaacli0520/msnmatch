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
from taggit.managers import TaggableManager
from PIL import ImageFilter

YEAR_CHOICES = (
			('1st year', '1st year'),
			('2nd year', '2nd year'),
			('3rd year', '3rd year'),
			('4th year', '4th year'),
		)
ROLE_CHOICES = (
			('Mentee', 'Mentee'),
			('Mentor', 'Mentor'),
		)
SEX_CHOICES = (
			('Male', 'Male'),
			('Female', 'Female'),
		)
MAJOR_CHOICES = (
('Accelerated B.A./Master of Public Policy (MPP) Program', 'Accelerated B.A./Master of Public Policy (MPP) Program'),
('Accounting', 'Accounting'),
('Aerospace Engineering', 'Aerospace Engineering'),
('African American & African Studies', 'African American & African Studies'),
('American Studies', 'American Studies'),
('Anthropology', 'Anthropology'),
('Architectural History', 'Architectural History'),
('Architecture', 'Architecture'),
('Art History', 'Art History'),
('Art, Studio', 'Art, Studio'),
('Astronomy', 'Astronomy'),
('Astronomy-Physics', 'Astronomy-Physics'),
('B.A. in Public Policy and Leadership', 'B.A. in Public Policy and Leadership'),
('B.S./M.S. in Teaching', 'B.S./M.S. in Teaching'),
('Bachelor of Science in Nursing (BSN)', 'Bachelor of Science in Nursing (BSN)'),
('Biology', 'Biology'),
('Biomedical Engineering', 'Biomedical Engineering'),
('Chemical Engineering', 'Chemical Engineering'),
('Chemistry', 'Chemistry'),
('Chinese Language & Literature', 'Chinese Language & Literature'),
('Civil Engineering', 'Civil Engineering'),
('Classics', 'Classics'),
('Cognitive Science', 'Cognitive Science'),
('Commerce', 'Commerce'),
('Comparative Literature', 'Comparative Literature'),
('Computer Engineering', 'Computer Engineering'),
('Computer Science', 'Computer Science'),
('Drama', 'Drama'),
('East Asian Studies', 'East Asian Studies'),
('Economics', 'Economics'),
('Electrical Engineering', 'Electrical Engineering'),
('Engineering Science', 'Engineering Science'),
('English', 'English'),
('Environmental Sciences', 'Environmental Sciences'),
('Environmental Thought & Practice', 'Environmental Thought & Practice'),
('Finance', 'Finance'),
('French', 'French'),
('German', 'German'),
('Global Studies', 'Global Studies'),
('History', 'History'),
('Human Biology', 'Human Biology'),
('Information Technology', 'Information Technology'),
('Italian', 'Italian'),
('Japanese Language & Literature', 'Japanese Language & Literature'),
('Jewish Studies', 'Jewish Studies'),
('Kinesiology', 'Kinesiology'),
('Latin American Studies', 'Latin American Studies'),
('Linguistics', 'Linguistics'),
('Management', 'Management'),
('Marketing', 'Marketing'),
('Mathematics', 'Mathematics'),
('Mechanical Engineering', 'Mechanical Engineering'),
('Media Studies', 'Media Studies'),
('Medieval Studies', 'Medieval Studies'),
('Middle Eastern and South Asian Languages and Cultures', 'Middle Eastern and South Asian Languages and Cultures'),
('Music', 'Music'),
('Neuroscience', 'Neuroscience'),
('Philosophy', 'Philosophy'),
('Physics', 'Physics'),
('Political Philosophy, Policy, and Law', 'Political Philosophy, Policy, and Law'),
('Political and Social Thought', 'Political and Social Thought'),
('Politics', 'Politics'),
('Psychology', 'Psychology'),
('RN to BSN', 'RN to BSN'),
('Religious Studies', 'Religious Studies'),
('Slavic Languages and Literatures', 'Slavic Languages and Literatures'),
('Sociology', 'Sociology'),
('South Asian Studies', 'South Asian Studies'),
('Spanish', 'Spanish'),
('Speech Communications Disorders Major', 'Speech Communications Disorders Major'),
('Statistics', 'Statistics'),
('Systems Engineering', 'Systems Engineering'),
('Teacher Education', 'Teacher Education'),
('Urban & Environmental Planning', 'Urban & Environmental Planning'),
('Women, Gender, and Sexuality', 'Women, Gender, and Sexuality'),
('Youth & Social Innovation Major', 'Youth & Social Innovation Major'),
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
	sex = models.CharField(max_length=20, choices = SEX_CHOICES, blank=True)
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
	video = models.FileField(upload_to="msn/video/", blank=True)
	role = models.CharField(max_length=255, choices=ROLE_CHOICES, blank=True)
	wechat = models.CharField(max_length=255, blank=True)

	def save(self, *args, **kwargs):
		# delete old file when replacing by updating the file
		try:
			this = Profile.objects.get(pk=self.pk)
			if self.picture and this.picture != self.picture:
				# this.picture.delete(save=False)
				tmp_picture = self.picture
				self.picture = self.compressImage(tmp_picture, False, 0, 0, 70)
				self.avatar = self.compressImage_new(tmp_picture, True, 60)
			if self.video and this.video != self.video:
				# this.video.delete(save=False)
				self.video.name = str(uuid.uuid4())
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

	def compressImage_new(self,uploadedImage, resize_bool, quality):
		imageTemporary = Image.open(uploadedImage)
		outputIoStream = BytesIO()
		if resize_bool:
			imageTemporary = imageTemporary.resize((int(imageTemporary.size[0]/10), int(imageTemporary.size[1]/10)), Image.LANCZOS)
		imageTemporary = imageTemporary.filter(ImageFilter.GaussianBlur(radius=10))
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
	# if this.picture:
	# 	this.picture.delete(save=False)
	# if this.video:
	# 	this.video.delete(save=False)

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

