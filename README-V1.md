
# QRSMS-V1

**Starting Project**

*Current Application link* : [https://qrsms-v1.herokuapp.com/](https://qrsms-v1.herokuapp.com/) 
This is extensively articulated because I tend to forget things, so this will help us all to document everything as we go through.

    python .manage.py createsuperuser --email admin@hassan11196.com --username admin11196

 password:

Two More Super Users Have been added.

**admin3755**

**admin3650**

Currently All models are in initial phase and database is SQLite. Our file management system is ephemeral. Which means that all changes that you make last as long as you keep the session active. We will move on to more permanent solutions as we progress.

Please read about naming conventions such as Camel Case,Pascal-Case,snake_case etc.

Please read about cookies and how basic auth works with authorization header. We will possibly shift to Oauth later on in the project.

All Endpoints as of version 1 require admin login. This will be processed using basic auth.

Current Endpoints are

- /admin

- /course_info

- /api-auth/login

- api-auth/logout

I suggest you play around with **course_info** and **admin** endpoints.

I have bundled a basic react app that fetches course using axios, Please learn how api request pagination works. And how to send auth parameters using axios.

Please read about web-pack, babel, transpilers. How web-pack bundles. Also read up on how loaders work for web-pack. I wasted too much time on that. CSS loaders are specially tricky to work with. Know the difference between Global CSS and CSS modules.

Read about difference between `--save-dev` and `--save` when installing dependencies using `npm`.

Nouman Bhai please see how serializers work and how we use the rest framework view-sets. and django-webpack-loader.

**How To Build and Run Project:** 

Clone the project into your System.

    git clone https://github.com/hassan11196/QRSMS-V1.git 

**For Back-End:**

Cd to QRSMS-V1 Folder.

Run the Following Command.

    pipenv shell

Cd to QRSMS

    python manage.py runserver

**For Front-end**

Open the initial_frontend folder and run the following command to first download dependencies

    npm install

and then to start the webserver.

    npm start

**Set Your Admin Authorization For Front-End.**

open the credential.js file in **initial_frontenc/src**

 

    const credential = {
    'REACT_APP_ADMIN_USERNAME':'YOUR ADMIN USERNAME HERE', 
    'REACT_APP_ADMIN_PASSWORD':'YOURADMIN PASSWORD HERE'
    } 

This is temporary. We will move to more secure methods as we progress.

**To build Web Pack Bundles.**

    ./node_modules/.bin/webpack --config webpack.config.js 

or Alternatively,

    npx webpack --config .webpack.config.js

**links :**

[React bundling with Django using Webpack 1
](https://owais.lone.pw/blog/webpack-plus-reactjs-and-django/) [React bundling with Django using Webpack 2
](https://www.easyaslinux.com/tutorials/devops/how-to-setup-reactjs-with-django-steps-with-examples/) 
[React bundling with Django using Webpack
](https://medium.com/labcodes/configuring-django-with-react-4c599d1eae63) [React Bootstrap Documentation](https://react-bootstrap.github.io/components/buttons/) [Django Rest Framework Tutorial](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5)