

# QRSMS-V1.4
Separated University, Campus, Department, Degree Classed to 'institution' app. 
CSRF Authentication ready to be implemented.
Session management needs to be worked on.
Included Ahsans Login Page to code base.

**links**:
[making-react-and-django-play-well-together-single-page-app-model](https://fractalideas.com/blog/making-react-and-django-play-well-together-single-page-app-model/)

[session-handling-in-react-with-redux-express-session-and-apollo-18j8](https://dev.to/tmns/session-handling-in-react-with-redux-express-session-and-apollo-18j8)

[local-storage-react](https://www.robinwieruch.de/local-storage-react)

[https://stackoverflow.com/questions/42420531/what-is-the-best-way-to-manage-a-users-session-in-react](https://stackoverflow.com/questions/42420531/what-is-the-best-way-to-manage-a-users-session-in-react)

[https://ltslashgt.com/2007/07/08/one-model-many-db-tables/](https://ltslashgt.com/2007/07/08/one-model-many-db-tables/)

[https://stackoverflow.com/questions/5036357/single-django-model-multiple-tables](https://stackoverflow.com/questions/5036357/single-django-model-multiple-tables)


# QRSMS-V1.3

Some changes have been made to `UserAdmin` to allow us to interact with new attributes of `User` in Django Admin.  
Added Django-Restful-admin. This will allow for admin access and manipulation to our React App Using Axios.
New Endpoint for this is as follows:

[*/rest_admin*](http://qrsms-v1.herokuapp.com/rest_admin)

This will branch into different models that are registered in admin.py file.

**links:**
Ahsan can ignore these.
[https://pypi.org/project/django-restful-admin/](https://pypi.org/project/django-restful-admin/)

[https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4](https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4)

[https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model](https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model)

[https://docs.djangoproject.com/en/2.2/ref/contrib/admin/actions/](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/actions/)

[https://docs.djangoproject.com/en/2.2/ref/contrib/admin](https://docs.djangoproject.com/en/2.2/ref/contrib/admin)

[https://docs.djangoproject.com/en/2.2/topics/auth/customizing/](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/)




# QRSMS-V1.2

  

**Moving Onwards**

The basic Django **User** model was replaced with **AbstractUser** that we will will used to create accounts for Students, Teachers and Faculty Members.

The Current Users had to be deleted and recreated(multiple times😢).

  
  
  
  

**Links:**

[Django Model Structure](https://simpleisbetterthancomplex.com/tips/2018/02/10/django-tip-22-designing-better-models.html)

[Models, Fields, Mangers, QuerySets, Backends Intro](https://medium.com/@jairvercosa/manger-vs-query-sets-in-django-e9af7ed744e0)

  

[Django QuerySets](https://simpleisbetterthancomplex.com/tips/2016/08/16/django-tip-11-custom-manager-with-chainable-querysets.html)

[Multiple User Models](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html)

[Django Custom Authorization](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#auth-custom-user)

  

[Serializers](https://medium.com/better-programming/how-to-use-drf-serializers-effectively-dc58edc73998)









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

](https://medium.com/labcodes/configuring-django-with-react-4c599d1eae63) [React Bootstrap Documentation](https://react-bootstrap.github.io/components/buttons/)  [Django Rest Framework Tutorial](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5)
