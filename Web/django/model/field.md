# Django - Model Fields

[Back](../index.md)

- [Django - Model Fields](#django---model-fields)
  - [Model Fields](#model-fields)
  - [Field options](#field-options)
  - [Example: Upload MP3 Files Using FileField](#example-upload-mp3-files-using-filefield)

---

## Model Fields

- `Model fields`:

  - the columns name of the mapped table.
  - The fields name should not be python reserve words like `clean`, `save` or `delete` etc.

- Django provides various built-in fields types:

  - ref: https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-types

- **Primary key**:

| Field            | Description                                         | Widget |
| ---------------- | --------------------------------------------------- | ------ |
| `AutoField()`    | An IntegerField that automatically increments.      |        |
| `BigAutoField()` | A 64-bit integer that automatically increments.     |        |
| `UUIDField()`    | A field for storing universally unique identifiers. |        |

- **Boolean**:

| Field            | Description         | Widget          |
| ---------------- | ------------------- | --------------- |
| `BooleanField()` | A true/false field. | `CheckboxInput` |

- **Integer**:

| Field                    | Description                           | Widget        |
| ------------------------ | ------------------------------------- | ------------- |
| `BigIntegerField()`      | A 64-bit integer                      | `NumberInput` |
| `IntegerField()`         | An integer field                      | `NumberInput` |
| `SmallIntegerField()`    | Like an IntegerField                  | `NumberInput` |
| `PositiveIntegerField()` | An integer field for zero or positive | `NumberInput` |

- **Decimal**:

| Field                                                | Description                      | Widget        |
| ---------------------------------------------------- | -------------------------------- | ------------- |
| `DecimalField(max_digits=None, decimal_places=None)` | A fixed-precision decimal number | `NumberInput` |
| `FloatField()`                                       | A floating-point number field    | `NumberInput` |

- **String**:

| Field                        | Description                                               | Widget      |
| ---------------------------- | --------------------------------------------------------- | ----------- |
| `CharField(max_length=None)` | A string field, for small- to large-sized strings.        | `TextInput` |
| `EmailField(max_length=254)` | A string field for email                                  | `TextInput` |
| `TextField()`                | A large text field.                                       | `Textarea`  |
| `GenericIPAddressField()`    | An IPv4 or IPv6 address string                            | `TextInput` |
| `URLField(max_length=200)`   | A CharField for a URL                                     | `URLInput`  |
| `SlugField(max_length=50)`   | A field for only letters, numbers, underscores or hyphens |             |
| `FilePathField()`            | Choices limited to the filenames in a certain directory   |             |

- **Date**:

| Field                                                | Description           | Widget          |
| ---------------------------------------------------- | --------------------- | --------------- |
| `DateTimeField((auto_now=False, auto_now_add=False)` | A date and time field | `DateTimeInput` |
| `DateField(auto_now=False, auto_now_add=False)`      | A date field          | `DateInput`     |
| `TimeField(auto_now=False, auto_now_add=False)`      | A time field.         | `TimeInput`     |
| `DurationField()`                                    | Periods of time.      |                 |

- **Data**:

| Field           | Description                         |
| --------------- | ----------------------------------- |
| `BinaryField()` | A field to store raw binary data.   |
| `JSONField()`   | A field to store JSON encoded data. |

- **File**:

| Field          | Description          | Widget                |
| -------------- | -------------------- | --------------------- |
| `FileField()`  | A file-upload field  | `ClearableFileInput.` |
| `ImageField()` | A image-upload field | `ClearableFileInput`  |

- **Relationship fields**

| Field                                             | Description                  |
| ------------------------------------------------- | ---------------------------- |
| `ForeignKey(to, on_delete)`                       | A many-to-one relationship.  |
| `ManyToManyField(to)`                             | A many-to-many relationship. |
| `OneToOneField(to, on_delete, parent_link=False)` | A one-to-one relationship.   |

---

## Field options

- a certain set of field-specific arguments

  - ref: https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-options

- **Constraint**

| Option             | Description            |
| ------------------ | ---------------------- |
| `primary_key`      | primary key            |
| `null`             | empty values           |
| `blank`            | allowed to be blank    |
| `choices`          | A choice sequence      |
| `default`          | default value          |
| `unique`           | unique values          |
| `unique_for_date`  | unique for date value  |
| `unique_for_month` | unique for month value |
| `unique_for_year`  | unique for year value  |

- **Meta**

| Option           | Description                 |
| ---------------- | --------------------------- |
| `db_column`      | column name                 |
| `verbose_name`   | A human-readable field name |
| `db_comment`     | comment on column           |
| `db_index`       | a database index            |
| `db_tablespace`  | tablespace name             |
| `editable`       | editability                 |
| `error_messages` | error messages              |
| `help_text`      | “help” text for widget      |
| `validators`     | A list of validators to run |

---

## Example: Upload MP3 Files Using FileField

- `HTML`:

```html
<!-- 
sets the value of enctype attribute: 
  assigns the uploaded file to request.FILE. Otherwise, the file will not be uploaded.
-->
<form
  id="form"
  action="__'music_test_upload'__"
  method="post"
  enctype="multipart/form-data"
>
  __csrf_token__

  <input id="music_name" name="music_name" class="form-control col-md-6 my-2" />

  <!-- 
sets name attribute as 'upload_file':
  the uploaded file can be achieved by the request.FILE["upload_file"]`
 -->
  <input
    id="file"
    type="file"
    class="form-control col-md-6 my-2"
    name="upload_file"
  />
  <button id="btn" class="btn btn-primary" type="submit">submit</button>
</form>
```

- `model_py`

```python
# the musice class represents the uploaded file in database.
# the FileField is actually the path storing the uploaded file.
# the 'upload_to' attribute:
#   the directory storing files.
#   default: ""
#   actual value is settings.MEDIA_ROOT.
#   example:  `upload_to='music/'` means the directory is `settings.MEDIA_ROOT/music/`。

class Music(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='music/')
```

- `view.py`

```python
def music_test_upload(request):
    ''' the view handles upload file page and stores the uploaded file '''
    context = {}
    html = "AppMusic/test.html"
    data = {}

    #when the submit method is post and a file has been submited.
    if request.method == 'POST' and request.FILES['upload_file']:
        music_name = request.POST["music_name"]
        upload_file = request.FILES['upload_file']    # get the uploaed file
        upload_file.name = music_name + ".mp3"        # modify the file name

        # kwag dict for Music model
        submit_data ={}
        submit_data["name"] = music_name
        submit_data["file"] = upload_file   # assign the uploaded file to the file field, whose type is FileField.

        try:
            new_music = Music(**submit_data)
            new_music.save()    # the uploaded file will be save into the target directory.
            print(new_music.file.url)
            data["success"] = "Successfully create a new record !"                 # response msg: success
        except Exception as error:                      # error
            data["error"] = str(error)                  # response msg: error

        context['data'] = data

    return render(request,html,context)

# Note:
# `new_music.file.url`：`FileField`类型的`url`属性是访问上存文件的url。该属性值是：`settings.MEDIA_URL` + `FileField`的`upload_to`属性 + `upload_file.name`。
# 当在前段需要引用上存文件时，可以直接使用`{{file.url}}`
# 注意：上存的文件与已存在的文件重名，django会自动修改新上存文件的文件名并自动记录在`FileField`字段中。
```

---

[TOP](#django---model-fields)
