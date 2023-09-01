# Django - Email

[Back](../index.md)

- [Django - Email](#django---email)
  - [`mail` module](#mail-module)
  - [Example: Preventing header injection](#example-preventing-header-injection)
  - [`EmailMessage` class](#emailmessage-class)
  - [Related Variables in `Settings.py`](#related-variables-in-settingspy)
  - [Example: Email](#example-email)

---

- Rel:
  - https://www.sitepoint.com/django-send-email/

## `mail` module

- `SMTP`
  - `the Simple Mail Transfer Protocol`
  - a set of rules for determining how emails are transferred from senders to recipients. SMTP servers use this protocol to send and relay outgoing emails.
  - port: 587

- `django.core.mail` module
  - Ref: https://docs.djangoproject.com/en/4.2/topics/email/


| Method                                                    | Description                                      |
| --------------------------------------------------------- | ------------------------------------------------ |
| `send_mail(subject, message, from_email, recipient_list)` | send email                                       |
| `send_mass_mail(datatuple)`                               | handle mass emailing                             |
| `mail_admins(subject, message)`                           | a shortcut to send an email to the site admins   |
| `mail_managers(subject, message)`                         | a shortcut to send an email to the site managers |

- Example

```py

from django.core.mail import send_mail, send_mass_mail

send_mail(
    "Subject",
    "Message.",
    "from@example.com",
    ["john@example.com", "jane@example.com"],
)
# subject: A string.
# message: A string.
# from_email: A string. If None, Django will use the value of the DEFAULT_FROM_EMAIL setting.
# recipient_list: A list of strings, each an email address. Each member of recipient_list will see the other recipients in the “To:” field of the email message.
# fail_silently: A boolean. When it’s False, send_mail() will raise an smtplib.SMTPException if an error occurs.

datatuple = (
    ("Subject", "Message.", "from@example.com", ["john@example.com"]),
    ("Subject", "Message.", "from@example.com", ["jane@example.com"]),
)

send_mass_mail(datatuple)
# datatuple is a tuple in which each element is in this format:
# (subject, message, from_email, recipient_list)

```

## Example: Preventing header injection

- The Django email functions outlined above all protect against header injection **by forbidding newlines** in header values. 
- If any `subject`, `from_email` or `recipient_list` contains a newline (in either Unix, Windows or Mac style), the email function will raise `django.core.mail.BadHeaderError` and, hence, will not send the email.

```py
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

def send_email(request):
    subject = request.POST.get("subject", "")
    message = request.POST.get("message", "")
    from_email = request.POST.get("from_email", "")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["admin@example.com"])
        except BadHeaderError:      # error if contains a newline
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("/contact/thanks/")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")
```

---

## `EmailMessage` class

- `EmailMessage` class
  - the class responsible for creating the email message.

- Parameter

| Parameter     | Description                                                    |
| ------------- | -------------------------------------------------------------- |
| `subject`     | The subject line of the email                                  |
| `body`        | The body text                                                  |
| `from_email`  | The sender’s address.                                          |
| `to`          | A list or tuple of recipient addresses.                        |
| `headers`     | A dictionary of extra headers to put on the message.           |
| `bcc`         | A list or tuple of addresses used in the “Bcc” header.         |
| `cc`          | A list or tuple of recipient addresses used in the “Cc” header |
| `connection`  | An email backend instance.                                     |
| `attachments` | A list of attachments to put on the message.                   |
| `reply_to`    | A list or tuple of recipient addresses                         |
  
- method

| Method          | Description                                               |
| --------------- | --------------------------------------------------------- |
| `send()`        | Sends the message. Return 1 if sent successfully.         |
| `message()`     | Constructs object holding the message.                    |
| `recipients()`  | Returns a list of all the recipients of the message       |
| `attach()`      | Creates a new file attachment and adds it to the message. |
| `attach_file()` | Creates a new attachment using a file.                    |


- Example

```py
from django.core.mail import EmailMessage

email = EmailMessage(
    "Hello",
    "Body goes here",
    "from@example.com",
    ["to1@example.com", "to2@example.com"],
    ["bcc@example.com"],
    reply_to=["another@example.com"],
    headers={"Message-ID": "foo"},
)

email.attach("design.png", img_data, "image/png")

email.attach_file("/images/weather_map.png")

email.send()
```

---

## Related Variables in `Settings.py`

| Variable               | Description                                                                                   | Default               |
| ---------------------- | --------------------------------------------------------------------------------------------- | --------------------- |
| `ADMINS`               | A list of all the people who get code error notifications                                     | `[]`                  |
| `MANAGERS`             | A list in the same format as `ADMINS` that specifies who should get broken link notifications | `[]`                  |
| `SERVER_EMAIL`         | The email address that error messages come from, such as those sent to ADMINS and MANAGERS.   | `root@localhost`      |
| `EMAIL_HOST`           | The host to use for sending email.                                                            | `localhost`           |
| `EMAIL_HOST_USER`      | Username to use for the SMTP server defined in `EMAIL_HOST`.                                  | `''`                  |
| `EMAIL_HOST_PASSWORD`  | Password to use for the SMTP server defined in `EMAIL_HOST`.                                  | `''`                  |
| `EMAIL_PORT`           | Port to use for the SMTP server defined in `EMAIL_HOST`.                                      | `25`                  |
| `DEFAULT_FROM_EMAIL`   | Default email address to use from the site manager(s).                                        | `webmaster@localhost` |
| `DEFAULT_CHARSET`      | Default charset used when constructing the Content-Type header                                | `utf-8`               |
| `EMAIL_BACKEND`        | The backend to use for sending emails.                                                        | `smtp.EmailBackend`   |
| `EMAIL_FILE_PATH`      | The directory used to store output files.                                                     | Not defined           |
| `EMAIL_SUBJECT_PREFIX` | Subject-line prefix for email messages.                                                       | `[Django] `           |
| `EMAIL_USE_LOCALTIME`  | Whether to send the SMTP Date header of email messages in the local time zone (True)          | `'[Django] '`         |
| `EMAIL_USE_TLS`        | Whether to use a TLS (secure) connection when talking to the SMTP server.                     | `False`               |
| `EMAIL_USE_SSL`        | Whether to use an implicit TLS (secure) connection when talking to the SMTP server.           | `False`               |
| `EMAIL_SSL_CERTFILE`   | The path used a PEM-formatted certificate chain file to use for the SSL connection            | `None`                |
| `EMAIL_SSL_KEYFILE`    | The path to a PEM-formatted private key file to use for the SSL connection.                   | `None`                |
| `EMAIL_TIMEOUT`        | Specifies a timeout in seconds for blocking operations like the connection attempt.           | `None`                |


- Email provider for `EMAIL_HOST`

| Email provider  | SMTP server host        |
| --------------- | ----------------------- |
| Gmail           | `smtp.gmail.com`        |
| Outlook/Hotmail | `smtp-mail.outlook.com` |
| Yahoo           | `smtp.mail.yahoo.com`   |

- `EMAIL_PORT`: 587
  - the default port for most SMTP servers.

- `EMAIL_USE_TLS`:
  - `Transport Layer Security (TLS)`: a security protocol used across the Web to encrypt the communication between web apps (Django) and servers (SMTP server).
  - defualt: `False`
  - `True`: Django will use Transport Layer Security to connect to the SMTP server and send emails.

---

## Example: Email

- Create App contact
- Configure variable in `settings.py`
  - create a `.env`, an file has email arguements.
  - Install `django-environ` package, with which `settings.py` can refer the arguement in `.env` file
  - Create setting variable for email.
- Create a form `ContactForm`
  - define a helping function to collect info
  - define a customized function `save()` to send email
- Create `ContactView` class, overriding form_valid() method in which email will be sent
- Create a `contact.html` to contain form and `success.html` to display message.

- Test: fill up the contact, then an email will be sent to the recipient.

---

- `.env`: a file with argument within the same folder as `settings.py`

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=test@gmail.com
EMAIL_HOST_PASSWORD=ojgkondpujxfcxao
RECIPIENT_ADDRESS=simonangelfong@gmail.com
```
- EMAIL_HOST: different email provider has different host.
- EMAIL_HOST_USER: full email address
- EMAIL_HOST_PASSWORD: can use the gmail app password
- RECIPIENT_ADDRESS: a customized address as recipient

---

- `pip install django-environ`

- `settings.py`

```py
import environ  # importing the environ package
# create an env object which will contain all the key–value pairs available on the .env file located in the folder where settings.py is.
env = environ.Env()
environ.Env.read_env()


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST")  # looking up the value EMAIL_HOST
EMAIL_PORT = 587  # using smtp protocol
EMAIL_USE_TLS = True  # using tls security protocol
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# a custom setting to send the emails to an address can be accessed.
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')
```

---

- Test in console:

```sh
py manage.py shell
```

```py
from django.core.mail import send_mail
from django.conf import settings
send_mail(
  subject='A cool subject',
  message='A stunning message',
  from_email=settings.EMAIL_HOST_USER,
  recipient_list=[settings.RECIPIENT_ADDRESS]
)
# return 1 if success
```

---

- `form.py`

```sh
from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(max_length=32)   # the name of inquirer
    # the subject of the inquiry message
    inquiry = forms.CharField(max_length=64)
    email = forms.EmailField()  # the email of inquirer
    message = forms.CharField(widget=forms.Textarea)  # the inquiry message

    def get_info(self):
        '''
        Method to return formatted info
        return: subject, msg
        '''
        # Calls the clean() method in the Form class
        cl_data = super().clean()

        # look up name in the cleaned data and strip to prevent newline character that might create header error.
        name = cl_data.get('name').strip()
        from_email = cl_data.get('email').strip()
        subject = cl_data.get('inquiry')
        message = cl_data.get('message')

        msg = f'{name} with email {from_email}:\n\n"{subject}"\n\n{message}'

        return subject, msg

    def send(self):
        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )

```

---

- `contact.html`

```html
// extends "layout/base.html" \\ // load bootstrap5 \\ // block main \\
<div class="mx-auto my-4 text-center">
  <h1>Contact Us</h1>
</div>
<div class="container">
  <form action="" method="post">
    // csrf_token \\ // bootstrap_form form \\ // buttons \\
    <button type="submit" class="btn btn-primary">Submit</button>
    // endbuttons \\
  </form>
</div>
// endblock \\
```

---

- `success.html`

```html
// extends 'layout/base.html' \\ // block main \\
<div class="mx-auto my-4 text-center">
  // for msg in messages \\ // if msg.level == DEFAULT_MESSAGE_LEVELS.SUCCESS \\
  <h1 class="fw-bolder text-success">__msg__</h1>
  // endif \\ // endfor \\
  <p class="my-5">
    You can send another in the
    <a href="// url 'contact:contact' \\">contact page</a>
  </p>
</div>
// endblock \\
```

---

[TOP](#django---email)
