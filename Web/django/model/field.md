# Django - Model Fields

[Back](../index.md)

- [Django - Model Fields](#django---model-fields)
  - [Model Fields](#model-fields)
  - [Field options](#field-options)

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

[TOP](#django---model-fields)
