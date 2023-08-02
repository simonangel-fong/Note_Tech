# Django - Meta

[Back](../index.md)

- [Django - Meta](#django---meta)
  - [Meta](#meta)
  - [Meta options](#meta-options)

---

## Meta

- `Meta`:
  - the Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural).
- None are required, and adding `class Meta` to a model is completely optional.

---

## Meta options

- Meta

| Meta Opt              | Description                                         |
| --------------------- | --------------------------------------------------- |
| `db_table`            | name of the database table                          |
| `verbose_name`        | A human-readable name for the object                |
| `verbose_name_plural` | The plural name for the object                      |
| `abstract`            | Wheter the current model is an abstract base class. |
| `db_table_comment`    | comment on the database table                       |
| `label`               | read-only, returns `app_label.object_name`          |
| `label_lower`         | read-only, returns `app_label.object_name`          |

- Contraint

| Meta Opt          | Description                                      |
| ----------------- | ------------------------------------------------ |
| `constraints`     | A list of constraints                            |
| `unique_together` | Sets of field names that must be unique together |

- index

| Meta Opt         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `indexes`        | A list of indexes                                     |
| `index_together` | Sets of field names that, taken together, are indexed |
| `db_tablespace`  | name of the database tablespace                       |

- Order

| Meta Opt        | Description                                                 |
| --------------- | ----------------------------------------------------------- |
| `ordering`      | order by                                                    |
| `get_latest_by` | name(s) of a field for `latest()` and `earliest()` methods. |

---

[TOP](#django---meta)
