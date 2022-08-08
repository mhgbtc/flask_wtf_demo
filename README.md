# flask_wtf_demo

## What is this ?

A simple app' demoing the usage of Flask-WTF, including a custom validator.

Flask-WTF is a lib that exists to help developers handle forms on Flask, IMHO, the 3 main things to consider when setting up basic HTML forms using this lib are:

- CSRF initialization and usage in HTML templates
- using the lib submit button type
- conditional behavior in controllers based on `if form.validate_on_submit()`
