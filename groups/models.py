from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill
import sys
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import uuid
from django.utils import timezone

GROUPROLE_CHOICES = (
			('Manager', 'Manager'),
			('Member', 'Member'),
		)
GROUPTYPE_CHOICES = (
			('Family', 'Family'),
			('Books', 'Books'),
			('Film and TV', 'Film and TV'),
			('General', 'General'),
			('Game', 'Game'),
			('Language', 'Language'),
			('Academic Interests', 'Academic Interests'),
			('Music', 'Music'),
			('Sport', 'Sport'),
			('Custom', 'Custom'),
		)

class Group(models.Model):
	group_users = models.ManyToManyField(User, through='GroupRelation')
	group_tags = models.ManyToManyField(Skill, through='TagRelation')
	group_name = models.CharField(max_length=30, blank=True)
	group_intro = models.TextField(max_length=500, blank=True)
	group_type = models.CharField(max_length=255, choices=GROUPTYPE_CHOICES, blank=True)
	picture = models.ImageField(upload_to="msn/image/group_pics/",blank=True)
	avatar = models.ImageField(upload_to="msn/image/group_pics/avatar/",blank=True)

	def __str__(self):
		return self.group_name

	def save(self, *args, **kwargs):
		# delete old file when replacing by updating the file
		try:
			this = Group.objects.get(pk=self.pk)
			if self.picture and this.picture != self.picture:
				# this.picture.delete(save=False)
				tmp_picture = self.picture
				self.picture = self.compressImage(tmp_picture, False, 0, 0, 70)
				self.avatar = self.compressImage_new(tmp_picture, True, 60)
		except: pass # when new photo then we do nothing, normal case
		super(Group, self).save(*args, **kwargs)


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


class GroupRelation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	group_role = models.CharField(max_length=255, choices=GROUPROLE_CHOICES, blank=True)

class TagRelation(models.Model):
	tag = models.ForeignKey(Skill, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class GroupFollowRelation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)


	