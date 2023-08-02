# Django - Relationship

[Back](../index.md)

- [Django - Relationship](#django---relationship)
  - [`Many-to-one` relationship](#many-to-one-relationship)
  - [`Many-to-many` relationships](#many-to-many-relationships)
    - [Intermediate Model](#intermediate-model)
  - [`One-to-one` relationships](#one-to-one-relationships)

---

## `Many-to-one` relationship

- use `django.db.models.ForeignKey`.
- `ForeignKey` requires a positional argument:

  - the class to which the model is related.

- Example:

```py
from django.db import models

class Manufacturer(models.Model):
    pass


class Car(models.Model):
    # it is suggested that the name of a foreign key field be the name of the model
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE
    )


    # it it fine that the name of a foreign key field uses a different name
    company_that_makes_it = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
    )

```

---

## `Many-to-many` relationships

- To define a many-to-many relationship, use `ManyToManyField`.
- `ManyToManyField` requires a positional argument:

  - the class to which the model is related.

- It doesn’t matter which model has the ManyToManyField, but you should only put it in one of the models – **not both**.

  - Generally, `ManyToManyField` instances should go in **the object that’s going to be edited on a form**.

- Example:

```py
from django.db import models

class Topping(models.Model):
    pass

class Pizza(models.Model):
    # a Topping can be on multiple pizzas and each Pizza has multiple toppings
    toppings = models.ManyToManyField(Topping)

# In the above example, toppings is in Pizza (rather than Topping having a pizzas ManyToManyField ) because it’s more natural to think about a pizza having toppings than a topping being on multiple pizzas. The way it’s set up above, the Pizza form would let users select the toppings.
```

---

### Intermediate Model

- `intermediate model`

  - the model is associated with the `ManyToManyField` using the through argument to point to the model that will act as an `intermediary`.

- Example:

```py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

# a group may have multiple persons. Relationship to person is created by intermediate model
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")  # using through argument target on intermediate model

    def __str__(self):
        return self.name

# intermediate model to represent complex relationship between persons and grouops, using ForeignKey
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

---

## `One-to-one` relationships

- To define a one-to-one relationship, use `OneToOneField`.

- `OneToOneField` requires a positional argument:

  - the class to which the model is related.

- Example:

```py
class MySpecialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    supervisor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supervisor_of",
    )
```

---

[TOP](#django---relationship)
