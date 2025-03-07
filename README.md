![](https://github.com/CheeseCake87/Flask-BigApp/blob/master/app/structures/default_theme/static/img/Flask-BigApp-Logo-white-bg.png)

# Flask-BigApp

`pip install flask-bigapp`

![Tests](https://github.com/CheeseCake87/Flask-BigApp/actions/workflows/tests.yml/badge.svg)

`NOTE:` This version; Being 1.4.* and above includes some breaking changes from anything on version 1.3.* and below.

## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, routes and models.
It has a few extra features built in to help with theming, securing pages and password authentication.

## Minimal Flask-BigApp app

A config file is required to sit next to your app's ```__init__.py``` file. This defaults to ```default.config.toml```

If Flask-BigApp is unable to find the `default.config.toml` file, it will create one.

You can also set the config file by setting the `BA_CONFIG` environment variable.
For example: (in terminal) `export BA_CONFIG=production.config.toml`

The ```default.config.toml``` file contains Flask config settings, a minimal version of this file looks like this:

```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "app"
version = "0.0.0"
secret_key = "super-secret-key"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
```

You can also use environment variables markers in the config file, here's an example:

```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "app"
version = "0.0.0"
secret_key = "<SECRET_KEY>"
debug = "<DEBUG>"
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
random_value = "<TAGS_CAN_BE_ANYTHING>"
```

Now if you set environment variables that are included in the tags, Flask-BigApp will replace them with the values.
Here's an example of setting environment variables in linux:

`export SECRET_KEY="super-secret-env-key"` and `export DEBUG=True`

The environment variables to pass in are defined in the config file, have a look at `random_value`.
To set this we will need to do: `export TAGS_CAN_BE_ANYTHING="what we put here will be the new value"`

**NOTE:** Some environment variable tags in the config file may not work if you are using `flask run`,
you can run the app by using `venv/bin/python run_example.py` instead.

Your app's ```__init__.py``` file should look like this:

```python
from flask import Flask
from flask_bigapp import BigApp

bigapp = BigApp()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)
    bigapp.import_builtins("routes")
    return main
```

**NOTE:** You can also manually set the config file by doing `bigapp.init_app(main, app_config_file="dev.config.toml")`

The ```bigapp.import_builtins("routes")``` method looks in the ```routes``` folder for ```.py``` files to import app routes
from.

Let's say we have this folder structure:

```
Flask-BigApp/
├── app/
│   ├── static/
│   ├── templates/
│   ├── routes/
│   │   └── index.py
│   ├── __init__.py
│   └── default.config.toml
├── venv
└── run.py
```

The ```index.py``` file should look like this:

```python
from flask import current_app


@current_app.route("/", methods=['GET'])
def index_page():
    """
    Example index route
    """
    return "You will see this text in the browser"
```

This file will get imported into the main app using the ```import_builtins()```method.

This is also the case if we add another file into the ```routes``` folder. Let's say we add ```my_page.py``` into the
routes folder, and it looks like this:

```python
from flask import current_app


@current_app.route("/my-page", methods=['GET'])
def my_page():
    """
    My Page Route
    """
    return "This is my page route"
```

So now our folder structure looks like this:

```
Flask-BigApp/
├── app/
│   ├── static/
│   ├── templates/
│   ├── routes/
│   │   ├── index.py
│   │   └── my_page.py
│   ├── __init__.py
│   └── default.config.toml
├── venv
└── run.py
```

The ```my_page.py``` routes will also be imported into the main app.

Using this method you can keep your routes in different files, and not have to worry about adding the import into
your ```__init__.py``` file.

## Adding values to the session

You can add values to Flask session from the config file, here's an example:

```toml
[flask]
app_name = "app"
version = "0.0.0"
secret_key = "super-secret-key"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true

[session]
my_session_value = "my session value"
```

Initialise the session values by doing the following:

```python
from flask import Flask
from flask_bigapp import BigApp

bigapp = BigApp()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)
    bigapp.import_builtins("routes")

    @main.before_request
    def before_request():
        bigapp.init_session()

    return main
```

## Setting up to work with models using SQLAlchemy

`NOTE:` The only accepted types of databases are: mysql / postgresql / sqlite / oracle

Flask-BigApp will also handle any binds. Any database settings added after the database.main section, will be added as a bind.

```toml
...
[database]
[database.main]
enabled = true
type = "sqlite"
database_name = "database"
location = "db"
port = ""
username = "user"
password = "password"

[database."defined_name"]
enabled = true
type = "sqlite"
database_name = "other_database"
location = "db"
port = ""
username = "user"
password = "password"
```

This is the same as the configuration:

```text
SQLALCHEMY_DATABASE_URI = 'sqlite:////absolute_app_path/db/database.db'
SQLALCHEMY_BINDS = {
    'defined_name': 'sqlite:////absolute_app_path/db/other_database.db',
}
```

## Importing Models

You can import model classes from a single file, of a folder of
model files by using the `bigapp.import_models(file="models.py", folder="models")` method.

Here's an example of how you can setup Flask-BigApp to import model classes:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)  # This will set the SQLALCHEMY_DATABASE_URI
    db.init_app(main)  # init the SQLAlchemy instance
    bigapp.import_builtins("routes")
    bigapp.import_models(file="models.py")
    # OR
    bigapp.import_models(folder="models")
    # OR
    bigapp.import_models(file="models.py", folder="models")
    return main
```

## Model Files

Here's an example of what a model file looks like:

```python
from app import db
from sqlalchemy import ForeignKey


class ExampleTable(db.Model):
    __tablename__ = "fl_example_table"
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('fl_example_user.user_id'))
    thing = db.Column(db.String(256), nullable=False)
```

## Working with the model_class method

Here's an example of how you can query using the `bigapp.model_class` method:
( this assumes you have `bigapp = BigApp()` in your apps `__init__.py` file )

```python
from flask import render_template

from app import db, bigapp
from .. import bp


@bp.route("/database-example", methods=["GET"])
def database_example():
    # Load the ExampleUser class found in the import_models folder, this way saves having to import files
    example_user = bigapp.model_class("ExampleUser")

    user_id = 1
    result = "NULL"
    find_username = True

    # Normal query
    nq_example_user = example_user.query

    # Query class using db.session
    sq_example_user = db.session.query(example_user)

    if find_username:
        sq_example_user = sq_example_user.filter(example_user.user_id == user_id).first()
        if sq_example_user is not None:
            username = sq_example_user.username
            result = f"Session Query: Username is {username}"

        nq_example_user = nq_example_user.filter(example_user.user_id == user_id).first()
        if nq_example_user is not None:
            username = nq_example_user.username
            example_table_join = nq_example_user.rel_example_table[0].thing
            result = f"{result}, Normal Query: Username is {username} -> ExampleTable Join: {example_table_join}"

    render = "blueprint1/database-example.html"
    return render_template(render, result=result)
```

## Importing Builtins (routes, template filters, context processors)

You can auto import routes, template filters, context processors, etc.. from a folder using:

- `bigapp.import_builtins("builtins")`

Here's an example of the builtins folder structure:

```text
builtins/
├── routes.py
└── template_filters.py
```

Importing builtins uses Flask's `current_app` to register the routes, here's an example of a file in the builtins folder:

```python
from flask import current_app
from flask import Response
from flask import render_template
from markupsafe import Markup


@current_app.template_filter('example')
def decorate_code(value: str) -> str:
    return Markup(f"The string value passed in is: {value} -> here is something after that value.")


@current_app.before_request
def before_request():
    pass


@current_app.errorhandler(404)
def request_404(error):
    return Response(error, 404)


@current_app.route("/builtin/route")
def builtin_route():
    render = "theme1/renders/builtin-route.html"
    return render_template(render)
```

## Importing Blueprints

You can auto import blueprints using:

- `bigapp.import_blueprints("blueprints")`

The shape of your folder to import blueprints from should look like this:

```text
blueprints/
├── blueprint1/
│   ├── routes/
│   │   └── index.py
│   ├── static/
│   ├── templates/
│   │   └── blueprint1/
│   │       └── index.html
│   ├── __init__.py
│   └── config.toml
└── another_blueprint/
    ├── routes/
    │   └── index.py
    ├── static/
    ├── templates/
    │   └── another_blueprint/
    │       └── index.html
    ├── __init__.py
    └── config.toml
```

In the above we are nesting all templates under a folder with the same name as the blueprint. This is a workaround to allow you to have template files with the
same names in different blueprint folders.

Blueprints require a config file to configure their settings. The config file should look like this:

```toml
enabled = "yes"

[settings]
url_prefix = "/"
template_folder = "templates"
static_folder = "static"
static_url_path = "/blueprint1/static"

[session]
var_in_session = "this can be loaded using bp.init_session()"
permissions = ["this", "that"]
logged_in = true
not_logged_in = false
```

`NEW IN 1.3.*`
Blueprint config.toml can also look like this:

```toml
enabled = "yes"
url_prefix = "/"

[session]
var_in_session = "this can be loaded using bp.init_session()"
permissions = ["this", "that"]
logged_in = true
not_logged_in = false
```

Using this method, bigapp will automatically look for and create the following folder structure:

```
blueprint1/
├── templates/ <- creates if not found/
│   └── blueprint1/ <- creates if not found
└── static/ <- creates if not found
```

The session section can be initialised using the `bp.init_session()` method. This places the values into the Flask session -> `from flask import session`

Here's an example of what your blueprints `__init__.py` file should look like:

```python
from flask_bigapp import Blueprint

bp = Blueprint(__name__, "config.toml")

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
```

Flask-BigApp inherits from Flask's Blueprint class in order to load from the config file. In the example above it states the config file name, however you can
omit this as it defaults to `config.toml`. Of course, you can specify your own config file name.

`bp.import_routes("routes")` method works much the same as `bigapp.import_builtins` except it is scoped to work with the blueprint object.

Here's an example of `routes/index.py`

```python
from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    render = bp.tmpl("index.html")

    return render_template(render)
```

The `bp.tmpl` method just decorates the string with the name of the blueprint, changing `"index.html"` to `"blueprint1/index.html"`.

Of course this only works if your templates are nested under a folder with the same name as your blueprint, however it does make it possible to change the
blueprint name later and not have to worry about search and replace.

## Importing Nested Blueprints

You can import nested blueprints from within a blueprint. Say our folder structure currently looks like this:

```text
blueprints/
└── blueprint1/
    ├── routes/...
    ├── static/...
    ├── templates/...
    ├── __init__.py
    └── config.toml
```

We can add a nested blueprint to the folder by doing the following:

```text
blueprints/
└── blueprint1/
    ├── nested_blueprint/
    │   ├── routes/
    │   │   └── index.py
    │   ├── static/
    │   ├── templates/
    │   │   └── nested_blueprint/
    │   │       └── index.html
    │   ├── __init__.py
    │   └── config.toml
    ├── routes/...
    ├── static/...
    ├── templates/...
    ├── __init__.py
    └── config.toml
```

You then import the nested blueprint in the parent blueprint's `__init__.py` file:

```python
# blueprint1's __init__.py file

from flask_bigapp import Blueprint

bp = Blueprint(__name__, "config.toml")

bp.import_routes("routes")
bp.import_nested_blueprint("nested_blueprint")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
```

This will now allow for using url_for like this:

`url_for("blueprint1.nested_blueprint.index")`

### Importing multiple nested blueprints

You can import multiple nested blueprints by placing the nested blueprints in a folder, here's an example folder structure:

```text
blueprints/
└── blueprint1/
    ├── nested_blueprints/
    │   ├── nested_blueprint1/
    │   │   ├── routes/...
    │   │   ├── static/...
    │   │   ├── templates/...
    │   │   ├── __init__.py
    │   │   └── config.toml
    │   └── nested_blueprint2/
    │       ├── routes/...
    │       ├── static/...
    │       ├── templates/...
    │       ├── __init__.py
    │       └── config.toml
    ├── routes/
    ├── static/
    ├── templates/
    ├── __init__.py
    └── config.toml
```

You then import the nested blueprints in the parent blueprint's `__init__.py` file:

```python
# blueprint1's __init__.py file

from flask_bigapp import Blueprint

bp = Blueprint(__name__, "config.toml")

bp.import_routes("routes")
# bp.import_nested_blueprint("nested_blueprint")
bp.import_nested_blueprints("nested_blueprints")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
```

## Creating a Blueprint via the CLI (NEW, BETA Feature)

You can create a blueprint via the CLI using:

`python3 -m flask_bigapp --add-bp-in "app/blueprints" --called "new_blueprint"`

This will create a new blueprint called `new_blueprint` and place it in the folder you specified. It creates the following folder structure:

```text
blueprints/
└── new_blueprint/
    ├── routes/
    │   └── index.py
    ├── templates/
    │   └── new_blueprint/
    │       └── index.html
    ├── static/
    ├── __init__.py
    └── config.toml
```

## Importing Structures (themes)

You can register structures (themes) from a folder using:

- `bigapp.import_structures("structures")`

Structures work the same as blueprints but are used for
theming and do not have the need for a config file or `__init__.py` file.

Here's an example of the folder layout of the `structures` folder:

```text
structures/
└── theme1/
    ├── static/
    │   ├── logo.png
    │   └── style.css
    └── templates/
        └── theme1/
            ├── extend/
            │   └── main.html
            ├── includes/
            │   └── footer.html
            └── macros/
                └── theme1_menu.html
```

Here's a few examples of how you would work with structures:

**extending a template:**

```html
{% extends "theme1/extend/main.html" %}
```

This would be placed at the top of a template file of a blueprint,
`blueprint1/templates/blueprint1/index.html` for exmaple.

**including a template:**

```html
{% include "theme1/includes/footer.html" %}
```

**including a macro:**

```html
{% import "theme1/macros/theme1_menu.html" as theme1_menu %}
```

**pulling a static file:**

```html
<img src="{{ url_for('theme1.static', filename='logo.png') }}" alt="logo">
```

A structures (themes) main purpose is to allow blueprints templates to work with structure blocks and static files.

Say, for example you set a blueprint template to extend a structure template, you can then use the structure blocks in the blueprint template.

```jinja
{% extends "theme1/extend/main.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Home</h1>
{% endblock %}
```

`theme1/extend/main.html` file:

```jinja
...

{% block title %}{% endblock %}

...

<body>

<div class="container">
    {% block content %}{% endblock %}
</div>

</body>

...
```

This allows for switching between structures, or working with similar structures.

# GitHub Project

This github project is a working example, and can do much more than the minimal app above.

This project covers how to work with models, blueprints and themes (structures)

### Linux setup

(Assuming location is home directory)

#### Git clone:

```bash
git clone https://github.com/CheeseCake87/Flask-BigApp.git
```

**OR**

1. Download zip and unpack
2. cd into unpacked folder

---
Move into the Flask-BigApp directory:

```bash
cd Flask-BigApp
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Enter virtual environment:

```bash
source venv/bin/activate
```

Install Flask-BigApp from src:

```bash
pip install -e .
```

Run Flask:

```bash
flask run
```

Or run from file:

```bash
python3 run_example.py
```
