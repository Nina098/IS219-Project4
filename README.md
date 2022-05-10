# IS219-Project4

# Workflows and Deployment

[![Development Workflow 3.8](https://github.com/Nina098/IS219-Project4/actions/workflows/dev.yml/badge.svg)](https://github.com/Nina098/IS219-Project4/actions/workflows/dev.yml)

* Development Deployment: https://lamastra-is219-project4-dev.herokuapp.com

[![Production Workflow 1](https://github.com/Nina098/IS219-Project4/actions/workflows/prod.yml/badge.svg)](https://github.com/Nina098/IS219-Project4/actions/workflows/prod.yml)

* Production Deployment: https://lamastra-is219-project4-prod.herokuapp.com

# Description
This is a simple web app that allows users to post and edit their recipes and view the recipes of other users. It was made for my IS219 class, which is a web development
class focused on building Flask applications.

To use the application, you must first register with an email and a password. You will then be directed to a form that allows you to add new recipes while editing or
deleting any you have already made. A recipe has a title and a text area to put in content. Titles do not have to be unique.

# Project 4 Requirements Met
* 25 unit tests (the test intended to test password validation, test_bad_register, is parameterized to 5 different tests to test every validator and
as a result is being counted as 5 tests)

* A registration form

* The ability to login and logout

* Some other functionality (adding, editing, and viewing recipes)