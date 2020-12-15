import os
import subprocess
import re
import platform

# Get application name
app_name = input('Enter the name of your application: ')
print(f'Creating {app_name}.')

# Create directory for the application
current_path = os.getcwd()
project_path = os.path.join(current_path, app_name)

try:
  os.mkdir(project_path)
except FileExistsError:
  raise FileExistsError(f'Directory with the name "{app_name}" already exists. Please choose a different name or remove the directory.')

os.chdir(project_path)
print(f'Creating app in path: {os.getcwd()}')

# Create and activate virtual env
subprocess.run(['python', '-m','venv', 'venv'])
if platform.system() == 'Windows':
  subprocess.run('venv\Scripts\\activate.bat')
else:
  subprocess.run(['source', 'venv/bin/activate'])

# Install Flask
try:
  subprocess.run(['pip', 'install', 'flask'])
except Exception:
  print(Exception)

# Create app
app_path = os.path.join(project_path, 'app')
os.mkdir(app_path)
os.chdir(app_path)

with open('__init__.py', 'w') as f:
  f.write("""
from flask import Flask

app = Flask(__name__)

from app import routes
""")

with open('routes.py', 'w') as f:
  f.write(f"""
from app import app
from flask import render_template, url_for

app_name = '{app_name}'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', app_name=app_name)
  """)

#Create templates directory and base and index templates
templates_path = os.path.join(app_path, 'templates')
os.mkdir(templates_path)
os.chdir(templates_path)

with open('base.html', 'w') as f:
  f.write("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css')}}">
    <title>{% block title %}{% endblock%}</title>
  </head>
  <body>
    {% block content %}
    {% endblock %}
  </body>
  <script src="{{ url_for('static', filename='main.js') }}"></script>
</html>
  """)

with open('index.html', 'w') as f:
  f.write("""
{% extends 'base.html' %}

{% block title %}
  {{ app_name }} - Index
{% endblock %}

{% block content %}
<div id="holder">
  <h1 id="hello">Hello, World!</h1><span class="span">from {{ app_name}}</span>
</div>
{% endblock %}
  """)

#Create static directory and Css and JavaScript files
static_path = os.path.join(app_path, 'static')
os.mkdir(static_path)
os.chdir(static_path)

with open('main.css', 'w') as f:
  f.write("""
body {
  margin: 0;
}

.holder {
  width: 100%;
  height: 600px;
  text-align: center;
  background-color: tomato;
  margin: 0;
}

.hello {
  margin: 0;
  padding-top: 10rem;
  color: yellow;
  font-size: 5rem;
}
  """)

with open('main.js', 'w') as f:
  f.write("""
const properHello = () => {
  document.getElementById('holder').className = 'holder';
  document.getElementById('hello').className = 'hello';
}

const timed = () => {
  setTimeout(properHello, 2000);
}

window.addEventListener('load', timed())
  """)

# Run the app!
os.chdir(project_path)
subprocess.run(['flask', 'run'])










 