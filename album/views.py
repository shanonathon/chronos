from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response,render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.conf import settings
from album.models import *
from photo.settings import MEDIA_URL
from album.forms import UploadFileForm
from django.template import RequestContext
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """Home Page."""
    if request.user.is_authenticated:
        return render(request, "album/home.html")
    else:
        return render(request, 'registration/login.html')   


@login_required
def main(request):
    """Main listing."""
    if request.user.is_authenticated:
        albums = Album.objects.all()
        if not request.user.is_authenticated():
            albums = albums.filter(public=True)

        paginator = Paginator(albums, 10)
        try: page = int(request.GET.get("page", '1'))
        except ValueError: page = 1

        try:
            albums = paginator.page(page)
        except (InvalidPage, EmptyPage):
            albums = paginator.page(paginator.num_pages)

        for album in albums.object_list:
            album.images = album.image_set.all()[:4]

        return render_to_response("album/list.html", dict(albums=albums, user=request.user,
            media_url=MEDIA_URL))
    else:
        return render(request, 'registration/login.html')

@login_required
def album_view(request, pk):
    """Album listing."""
    album = Album.objects.get(pk=pk)
    if not album.public and not request.user.is_authenticated():
        return HttpResponse("Error: you need to be logged in to view this album.")

    images = album.image_set.all()
    paginator = Paginator(images, 30)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)

    return render_to_response("album/album.html", dict(album=album, images=images, user=request.user,
        media_url=MEDIA_URL))    

@login_required
def image_view(request, pk):
    """Image page."""
    img = Image.objects.get(pk=pk)
    return render_to_response("album/image.html", dict(image=img, user=request.user,
          media_url=MEDIA_URL))


class UploadView(CreateView):
    template_name = 'album/upload.html'
    form_class = UploadFileForm


    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')

    def get_success_url(self):
        return reverse('album:home')
