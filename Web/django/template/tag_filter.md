# Django - Built-in template tags and filters

[Back](../index.md)

- [Django - Built-in template tags and filters](#django---built-in-template-tags-and-filters)
  - [Built-in tag](#built-in-tag)
  - [Built-in filter](#built-in-filter)
  - [Template-tag Libraries](#template-tag-libraries)
    - [`django.contrib.humanize`](#djangocontribhumanize)
    - [`static`](#static)

---

## Built-in tag

- Ref:

  - https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#built-in-tag-reference

- **HTML Escaping**

| Tag          | Description                                  |
| ------------ | -------------------------------------------- |
| `autoescape` | Controls the current auto-escaping behavior. |

- **Template Inheritance**

| Tag       | Description                                               |
| --------- | --------------------------------------------------------- |
| `block`   | Defines a block to be overridden by child templates       |
| `extends` | Signals that this template extends a parent template      |
| `include` | Loads a template and renders it with the current context. |
| `load`    | Loads a custom template tag set.                          |

- **Flow Control**

| Tag           | Description                                                    |
| ------------- | -------------------------------------------------------------- |
| `for`         | Loops over each item in an array                               |
| `for … empty` | A `for` tag can take an optional `empty` clause                |
| `if`          | evaluates a variable                                           |
| `ifchanged`   | Check if a value has changed from the last iteration of a loop |

- **Content Filter**

| Tag          | Description                                                                            |
| ------------ | -------------------------------------------------------------------------------------- |
| `cycle`      | Produces one of arguments each time when encountered                                   |
| `resetcycle` | Resets a previous cycle so that it restarts from its first item at its next encounter. |
| `filter`     | Filters the contents                                                                   |
| `firstof`    | Outputs the first argument variable that is not “false”                                |
| `regroup`    | Regroups a list of alike objects by a common attribute.                                |

- **Other**

| Tag          | Description                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `comment`    | Comment tags                                                             |
| `csrf_token` | Cross Site Request Forgery protection                                    |
| `lorem`      | Displays random “lorem ipsum” Latin text.                                |
| `now`        | Displays the current date and/or time                                    |
| `spaceless`  | Removes whitespace between HTML tags.                                    |
| `url`        | Returns an absolute path reference.                                      |
| `verbatim`   | Stops the template engine from rendering the contents of this block tag. |
| `widthratio` | calculates the ratio                                                     |
| `with`       | Caches a complex variable under a simpler name.                          |

---

## Built-in filter

- Ref:

  - https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#built-in-filter-reference

- Syntax:

  ```django
  {{ var_name | filter: argument1, argument2}}
  ```

- **Number**

| Filter        | Description                                             |
| ------------- | ------------------------------------------------------- |
| `add`         | Adds the argument to the value.                         |
| `divisibleby` | Returns True if the value is divisible by the argument. |
| `floatformat` | Rounds a number to decimal places.                      |
| `get_digit`   | Returns the requested digit                             |

- **String**

| Filter               | Description                                                                          |
| -------------------- | ------------------------------------------------------------------------------------ |
| `safe`               | Marks a string as not requiring further HTML escaping prior to output.               |
| `escape`             | Escapes a string’s HTML.                                                             |
| `force_escape`       | Applies HTML escaping to a string                                                    |
| `default`            | If value evaluates to `False`, uses the given default.                               |
| `default_if_none`    | If (and only if) value is None, uses the given default.                              |
| `stringformat`       | Formats the variable according to the argument, a string formatting specifier.       |
| `capfirst`           | Capitalizes the first character of the value.                                        |
| `title`              | Makes words start with an uppercase character and the remaining characters lowercase |
| `upper`              | Converts a string into all uppercase.                                                |
| `lower`              | Converts a string into all lowercase.                                                |
| `cut`                | Removes all values of arg from the given string.                                     |
| `addslashes`         | Adds slashes before quotes. Useful for escaping strings in CSV.                      |
| `linebreaks`         | Replaces line breaks in plain text with appropriate HTML                             |
| `linebreaksbr`       | Converts all newlines in a piece of plain text to HTML line breaks (`<br>`).         |
| `linenumbers`        | Displays text with line numbers.                                                     |
| `center`             | Centers the value in a field of a given width.                                       |
| `ljust`              | Left-aligns the value in a field of a given width.                                   |
| `rjust`              | Right-aligns the value in a field of a given width.                                  |
| `yesno`              | Maps values for `True`, `False`, and (optionally) `None`, to the strings             |
| `striptags`          | Makes all possible efforts to strip all HTML tags.                                   |
| `truncatechars`      | Truncates a string if it is longer than the specified number                         |
| `truncatechars_html` | Truncates HTML tags if it is longer than the specified number                        |
| `truncatewords`      | Truncates a string after a certain number of words                                   |
| `truncatewords_html` | Truncates HTML tags after a certain number of words                                  |
| `wordcount`          | Returns the number of words.                                                         |
| `wordwrap`           | Wraps words at specified line length.                                                |
| `filesizeformat`     | Formats the value like a ‘human-readable’ file size                                  |
| `length`             | Returns the length of the value.                                                     |
| `length_is`          | Returns True if the value’s length is the argument                                   |
| `phone2numeric`      | Converts a phone number (possibly containing letters) to its numerical equivalent.   |
| `pluralize`          | Returns a plural suffix                                                              |
| `slugify`            | Converts to ASCII. Converts spaces to hyphens.                                       |

- **List**

| Filter             | Description                                                               |
| ------------------ | ------------------------------------------------------------------------- |
| `safeseq`          | Applies the safe filter to each element of a sequence.                    |
| `make_list`        | Returns the value turned into a list.                                     |
| `first`            | Returns the first item in a list.                                         |
| `last`             | Returns the last item in a list.                                          |
| `random`           | Returns a random item from the given list.                                |
| `slice`            | Returns a slice of the list.                                              |
| `dictsort`         | returns sorted a list of dictionaries by the key.                         |
| `dictsortreversed` | returns sorted a list of dictionaries in reverse order by the key.        |
| `join`             | Joins a list with a string.                                               |
| `unordered_list`   | Returns an HTML unordered list – WITHOUT opening and closing `<ul>` tags. |

- **Url**

| Filter        | Description                                                                           |
| ------------- | ------------------------------------------------------------------------------------- |
| `iriencode`   | Converts an IRI (Internationalized Resource Identifier) to a string suitable for URL. |
| `urlencode`   | Escapes a value for use in a URL.                                                     |
| `urlize`      | Converts URLs and email addresses in text into clickable links.                       |
| `urlizetrunc` | Truncates URLs longer than the given character limit.                                 |

- **Date Time**

| Filter      | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| `date`      | Formats a date according to the given format.                |
| `time`      | Formats a time according to the given format.                |
| `timesince` | Formats a date as the time since that date                   |
| `timeuntil` | measures the time from now until the given date or datetime. |

- **Code**

| Filter        | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `escapejs`    | Escapes characters for use as a whole JavaScript string literal      |
| `json_script` | Safely outputs a Python object as JSON, wrapped in a `<script>` tag. |

---

## Template-tag Libraries

### `django.contrib.humanize`

- A set of Django template filters useful for adding a “human touch” to data.

- Ref:
  - https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#static

| Tag           | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `apnumber`    | For numbers 1-9, returns the number spelled out.                     |
| `intcomma`    | Converts an integer or float to a string with commas.                |
| `intword`     | Converts a large integer to a friendly text representation.          |
| `naturalday`  | Return “today”, “tomorrow” or “yesterday                             |
| `naturaltime` | Returns a string representing how many seconds, minutes or hours ago |
| `ordinal`     | Converts an integer to its ordinal as a string.                      |

---

### `static`

- enable in template with the ** load ** tag.

| Tag                 | Description                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------- |
| `static`            | Links to static files that are saved in `STATIC_ROOT` Django ships with a `static` template tag |
| `get_static_prefix` | populates a template variable with the media prefix `STATIC_URL`                                |
| `get_media_prefix`  | populates a template variable with the media prefix `MEDIA_URL`                                 |

---

[TOP](#django---built-in-template-tags-and-filters)
