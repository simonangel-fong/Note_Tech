# Django - ModelForm

[Back](../index.md)

- [Django - ModelForm](#django---modelform)
  - [`ModelForm`](#modelform)
    - [Example: Create Form class from model](#example-create-form-class-from-model)
  - [Field types](#field-types)
  - [`save()` method](#save-method)
  - [Meta Class](#meta-class)

---

## `ModelForm`

-  `ModelForm`
   -  a class which is used to create an HTML form by using the Model.
   -  an efficient way to create a form without writing HTML code.

- `Meta`
  - an inner class provides information connecting the model to the form.

- Syntax:
```py
class Model_Form(ModelForm):
    # some form fields
    class Meta:
        model = model_name
        fiels = []
        # some info about this form, such as help_texts ro widgets
```


### Example: Create Form class from model

- Example:

```py
from django.forms import ModelForm
from myapp.models import Article

# Create the form class.
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["pub_date", "headline", "content", "reporter"]

# Creating a form to add an article.
form = ArticleForm()

# Creating a form to change an existing article.
article = Article.objects.get(pk=1)
form = ArticleForm(instance=article)
```
---

## Field types

- **Auto ID**

| Model field      | Form field                  |
| ---------------- | --------------------------- |
| `AutoField`      | Not represented in the form |
| `BigAutoField`   | Not represented in the form |
| `SmallAutoField` | Not represented in the form |

- **Number**

| Model field                 | Form field                            |
| --------------------------- | ------------------------------------- |
| `BooleanField`              | `BooleanField`, or `NullBooleanField` |
| `IntegerField`              | `IntegerField`                        |
| `PositiveIntegerField`      | `IntegerField`                        |
| `BigIntegerField`           | `IntegerField`                        |
| `PositiveBigIntegerField`   | `IntegerField`                        |
| `SmallIntegerField`         | `IntegerField`                        |
| `PositiveSmallIntegerField` | `IntegerField`                        |
| `FloatField`                | `FloatField`                          |


- **String**

| Model field             | Form field                             |
| ----------------------- | -------------------------------------- |
| `BinaryField`           | `CharField`                            |
| `CharField`             | `CharField`                            |
| `EmailField`            | `EmailField`                           |
| `FilePathField`         | `FilePathField`                        |
| `IPAddressField`        | `IPAddressField`                       |
| `GenericIPAddressField` | `GenericIPAddressField`                |
| `JSONField`             | `JSONField`                            |
| `SlugField`             | `SlugField`                            |
| `TextField`             | `CharField` with widget=forms.Textarea |
| `URLField`              | `URLField`                             |
| `UUIDField`             | `UUIDField`                            |

- **Date**

| Model field     | Form field      |
| --------------- | --------------- |
| `DateField`     | `DateField`     |
| `DateTimeField` | `DateTimeField` |
| `DecimalField`  | `DecimalField`  |
| `DurationField` | `DurationField` |
| `TimeField`     | `TimeField`     |

- **File**

| Model field  | Form field   |
| ------------ | ------------ |
| `FileField`  | `FileField`  |
| `ImageField` | `ImageField` |

- **Relationship**

| Model field       | Form field                 |
| ----------------- | -------------------------- |
| `ForeignKey`      | `ModelChoiceField`         |
| `ManyToManyField` | `ModelMultipleChoiceField` |

---

## `save()` method

- Example: Create and update


```py
from myapp.models import Article
from myapp.forms import ArticleForm

# Create a form instance from POST data.
f = ArticleForm(request.POST)

# Save a new Article object from the form's data.
new_article = f.save()

# Create a form to edit an existing Article, but use
# POST data to populate the form.
a = Article.objects.get(pk=1)
f = ArticleForm(request.POST, instance=a)
f.save()    # update
```

- Example: save the many-to-many form data

```py
# Create a form instance with POST data.
f = AuthorForm(request.POST)

# Create, but don't save the new author instance.
new_author = f.save(commit=False)

# Modify the author in some way.
new_author.some_field = "some_value"

# Save the new instance.
new_author.save()

# Now, save the many-to-many data for the form.
f.save_m2m()
```

---

## Meta Class

| Attributes         | Description                                        |
| ------------------ | -------------------------------------------------- |
| `model`            | the model to refer to                              |
| `fields`           | the fields used in the form. `__all__`: all fields |
| `exclude`          | fields to be excluded                              |
| `widgets`          | a dictionary mapping field names to widget         |
| `labels`           | a dictionary mapping field names to label tag      |
| `help_texts`       | a dictionary mapping field names to help_texts     |
| `error_messages`   | a dictionary mapping field names to errors         |
| `field_classes`    | a dictionary mapping field names to type of fields |
| `localized_fields` | a list of field names to  localize data            |

```py
from django.utils.translation import gettext_lazy as _

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["name", "title", "birth_date"]
        labels = {
            "name": _("Writer"),
        }
        help_texts = {
            "name": _("Some useful help text."),
        }
        error_messages = {
            "name": {
                "max_length": _("This writer's name is too long."),
            },
        }
```

---

[TOP](#django---modelform)