from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.files import File
from os.path import join as pjoin
from tempfile import *
import os
from PIL import Image as PImage
from django.conf import settings
from string import join
from photo.settings import MEDIA_ROOT

class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    cover = models.FileField(upload_to="images/",default=None,null=True)
    def __unicode__(self):
        return self.title

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tag

class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))

    def thumbnail(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (
                                                                    (self.image.name, self.image.name))
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size

        # large thumbnail
        fn, ext = os.path.splitext(self.image.name)
        im.thumbnail((128,128), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
        tf2.close()


        super(Image, self).save(*args, ** kwargs)


    def get_next(self):
        next = Image.objects.filter(id__gt=self.id)
        if next:
            return next[0]
        return False


    def get_prev(self):
        prev = Image.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return False    
