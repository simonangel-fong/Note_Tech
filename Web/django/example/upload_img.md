# Django - Upload Image

[Back](../index.md)

- [Django - Upload Image](#django---upload-image)
  - [Functionality: Upload Image](#functionality-upload-image)
  - [Functionality: List Images](#functionality-list-images)

---

## Functionality: Upload Image

- `Settings.py`

```py
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')
```

- `models.py`

```py
from django.db import models

# the function to customize file name
def img_upload_to(instance, filename):
    return f"image/{instance.img_name}.png"

class ImageFile(models.Model):
    img_name = models.CharField(
        max_length=64,
        unique=True
    )
    img_file = models.ImageField(
        upload_to=img_upload_to
    )
```

- `forms.py`

```py
from .models import ImageFile
from django import forms


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = "__all__"

```

- `views.py`

```py
def img_upload(request):
    ''' upload '''
    context = {}
    if request.method == "POST":
        form = ImageFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("img_list")
        else:
            context["error"] = form.errors.as_text()
    form = ImageFileForm()      # create a empty form
    context["form"] = form
    template = "AppImage/img_upload.html"
    return render(request, template, context)
```

- `urls.py`

```py
from django.urls import path
from AppImage import views

urlpatterns = [
    path("list", view=views.img_list, name="img_list"),
    path("upload", view=views.img_upload, name="img_upload"),
    ]
```

- `img_upload.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    {% if error %}
    <p>{{error}}</p>
    {% endif %}
    <form method="post" enctype="multipart/form-data">
      {% csrf_token %} {{form.as_p}}
      <button type="submit">Submit</button>
    </form>
  </body>
</html>
```

---

## Functionality: List Images

- `views.py`

```py
def img_list(request):
    ''' list '''
    data = ImageFile.objects.all()
    template = "AppImage/img_list.html"
    context = {
        "data": data
    }
    return render(request, template, context)
```

- `urls.py`

```py
from django.conf import settings
from django.conf.urls.static import static

# the url configuration to access to media files
if settings.DEBUG == True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

```

- `img_list.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <a href="{% url 'img_list' %}">Image List</a>
    <a href="{% url 'img_upload' %}">Image Uploaded</a>
    {% if data %} {% for img in data %}
    <ul>
      <li>
        <a href="{% url 'img_detail' img.img_name %}"> {{img.img_name}} </a>
      </li>
    </ul>

    {% endfor %} {% else %}
    <p>No data.</p>
    {% endif %}
  </body>
</html>
```

---

[TOP](#django---upload-image)