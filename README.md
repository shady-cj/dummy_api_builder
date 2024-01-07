# DummyApi Builder
## "Easily create API, Streamline your work flow with ease, Confidence in data manipulation and Data managment."


## Features

- [x] Supports GET, POST, PUT and DELETE requests
- [x] Generates random REST API endpoints 
- [x] Allows customization of endpoint paths
- [x] Can generate string, number, date data types
- [x] Ability to create relationships such as foreign key
- [x] Ability to add multiple primary key fields and other common constraints 
- [x] Generates sample JSON response bodies 
- [x] Option to save and load API definitions
- [x] Integration with API tools
- [x] Modeling of relationships between API resources 

## Why You Should Use DummyApi

| --- | :---: | :---: | :---: |


| 📆 Reusable |  | | ✓ |

| 🌈 Facilitate | | | ✓ |

| 🗣️ Saves Time | | | ✓ |

| 🏷 Increases Productivity | | | ✓ |

| 📝 Easy Integration | | | ✓ |

| 🎡 Easy to Use | |  | ✓ |

| 🚦 Documentation | |  | ✓ |

| 🍰 Flexibility | | | ✓ |



## Contents
- [Overview](#overview) 
- [Requirements](#requirements)
- [Who this is for?](#who-this-is-for)
- [Limitations](#limitations)
- [Setting Up](#setting-up)
- [Using the application](#using-the-application)
    - [Creating an API](#creating-an-api)
    - [Adding a Model to the API](#adding-a-model-to-the-api)
    - [Updating api and models](#updating-api-and-models)
    - [Deleting api and models](#deleting-api-and-models)
## Overview
### Easily Create API
With our powerful web application, you'll effortlessly create APIs in no time, empowering you to perform essential CRUD operations (Create, Retrieve, Update, Delete) on your data.

### Streamline Your Workflow with Ease
Effortlessly define your API structure, model your data, and let Dummy API builder handle the heavy lifting, so you can enjoy a streamlined workflow.

### Confidence in Data Manipulation
Dummy API builder equips you with the tools and functionality to manipulate your data confidently. It gives you full control over your data management tasks.

### Data Management
It offers an intuitive approach, eliminating unnecessary complexities and time-consuming processes. With Dummy API builder, you can make the most of your data without hassle.


## Requirements
- Basic Programming knowledge
- Basic API knowledge(how to define relationships)

## Who this is for
This tool allows you to create simple apis for consumption, thus providing a quick way of creating an api, and simple relationships. This tool is useful for 
- Frontend Developers who needs to quickly create an endpoint for testing the applications
- Backend developers who wants to create a large scale api and need to breakdown the workflow into simpler units (You can quickly create simple apis and create relationship between this apis for testing purposes in order to envision how to build the larger api service)
- Can be used in very small scale applications.

## Limitations
This tool is simple tool and you can also infer that from the title of the project. So before you consider using it here are the limitations
- Cannot be used in medium-large scale applications
- Cannot be used in small-scale applications that requires very complex api relationship
- Relationships such as many-many and one-one isn't implemented in v1(perhaps in v2)
- Rigidity in how you get back your data (little or no flexibilty to run complex queries) (perhaps in the coming versions)
- Endpoints are fixed and enforces strictly you follow the format in order to make most use of the api (we'll see that in the usage section of this docs)
- This application is still being tested and might break at any point

## Setting up
As at the writing of this docs, the application hasn't been fully deployed into production so to test it you might have to configure it yourself, 
which is a very simple process. For this project to work properly you'll need both the frontend and backend fully running. To run locally you must have python (version 3.6 and above) and node (preferably version 18 and above) installed on your machine
### Steps
- clone the project repo.
- change directory into the backend, create a virtual environment(if necessary and activate) then run `pip install -r requirements.txt`. It might be important to use a virtual environment to avoid conflicting with your installed packages.
- Create a `.env` file in the backend folder and create an environment variable for the secret key for encoding sessions(Jwt).
```
SECRET=<random_value>
```
- After full installation of the dependencies fully, run `python3 -m api.v1.app` on windows simply use `python` instead and you should have your application running in `debug mode`

![Ubuntu22 04 (Snapshot 8)  Running  - Oracle VM VirtualBox 6_23_2023 7_50_44 AM (2)](https://github.com/shady-cj/dummy_api_builder/assets/66220414/c6531749-41b4-4868-8871-84023454f22f)

![Ubuntu22 04 (Snapshot 8)  Running  - Oracle VM VirtualBox 6_23_2023 7_51_47 AM (2)](https://github.com/shady-cj/dummy_api_builder/assets/66220414/f4278149-cbaa-4a3c-b0bd-c466e1e328df)

- Also cd into frontend/dummy_api_frontend/
- run `npm install`
- Afterwards run `npm run dev`
- To let the frontend know about the backend create a `.env` file in the folder where you run `npm install` and add an environment variable in the file
  ```
  VITE_HOST_URL=http://127.0.0.1:5900
  ```
  Depending on the interface your backend app is running but most likely it'll be localhost `127.0.0.1` but if you're like me and you want to run the backend from a virtual machine and the frontend on your desktop, substitute the ip with the ip address exposed by your virtual machine. The port by default is `5900` you can change that by editing the `app.py` in `backend/api/v1` and make sure to update the port in your frontend `.env` file. Then your application should be up and running, you can go ahead and create an account and login. By default it uses a sqlite database you can also change that if you're familiar with sql alchemy by editing the line
  ```
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
  ```
  in `backend/api/v1/app.py`

## Using the application

### Creating an API
Go ahead and create an account and login.![daB - Google Chrome 6_26_2023 12_41_21 PM (2)](https://github.com/shady-cj/dummy_api_builder/assets/66220414/61b3b107-578a-4861-8bff-2dbefaf73ac5)

Creating an api is easy, navigate to the create api page and provide the name of the api (required) and the description (optional).

![daB - Google Chrome 6_26_2023 12_53_24 PM (2)](https://github.com/shady-cj/dummy_api_builder/assets/66220414/032db2bb-d434-475c-a390-0736fbfa8005)

![daB - Google Chrome 6_26_2023 12_53_48 PM (2)](https://github.com/shady-cj/dummy_api_builder/assets/66220414/f95e83f5-45f9-4460-b6f4-319d791f2a55)

#### :warning: IMPORTANT NOTE

While creating an api, all names(like api name, model name, field name) must be a valid python identifier, not a [python keyword](https://www.w3schools.com/python/python_ref_keywords.asp) and must be atleast 3 characters.
To know about python identifiers here is an [article](https://www.digitalocean.com/community/tutorials/python-keywords-identifiers) to understand more.

### Adding a Model to the API
To add a model to the API here are the fields to fill:
- **Model Name**: Name of the model (required).
- **Description**: The description of the model (optional).

These are the basic information needed. But that's not enough to create a model. Suppose we wanted to create a Model in Python(Flask or Django) we'll have something like this.
```
class User(db.Model):
  _id = db.IntegerField()
  name = db.StringField()
  email = db.EmailField()
```
To create a model field, you can just click on the `Add Field` button, the necessary information to provide are:
- **Field Name**:
    - Field is required
    - The name of the model field(e.g _id, name, email).
    - Must be a valid python identifier
    - Must be atleast 3 characters or more.
    - if you need to have an `id` use `_id` instead.
    - Mustn't be a python keyword
- **Max Length**:
    - Field is optional
    - The maximum length of characters (This only works for string or text data types)
- **Field Data Type**:
    - Field is required 
    - Integer: Valid integers only (no decimals or floats)
    - String: Any string (if you need to store strings that would be greater than 100 characters, you should use the Text data type)
    - Text: Large texts (e.g descriptions, rich texts etc...)
    - Boolean: Takes only true of false value (format ("True" | "False") )
    - Date: Takes any valid date look at valid date formats in python [here](https://www.geeksforgeeks.org/how-to-format-date-using-strftime-in-python/)
    - Datetime: Same as date look at valid formats [here](https://www.programiz.com/python-programming/datetime)
- **Constraints**:
    - Field is optional
    - More than one constraints can be selected
    - Primary Key: 
        - There must be atleast a field with this option selected (The model won't be created if not)
        - There can be more than one primary key for a model. (The behavior is it concatenates the fields together in the other they were marked primary keys, e.g _id+email="1example@gmail.com").
    - Foreign Key:
        - if this model field is tagged as a foreign key then it's mandatory to fill up the `Foreign Key Reference Table`
        - Creates a relationship with another table, which can be in another api. 
    - Unique: Ensures that the field is unique
    - Nullable:
        - Ensures that the field can be null
        - if you already add a key to be primary key you cannot mark it to be nullable, if such happens the nullable constraint would be dropped
- **Foreign Key Reference Table**:
    - Field is optional, mandatory if the model field has a `Foreign Key` constraints.
    - Uses the `api.table` format
    - `api` refers to the api to create the relationship with, The api must be an existing api created by the user
        - `api` can be the api in which the current model resides or any other api owned by the user on the application.
    - `table` refers to the model/table to create the relationship with, The table must be an existing table
        - Remember `table` you use must be present on the `api` referenced.

**Date & Datetime** are validated through dateutil.parser so any valid `strftime()`(for python) formatted date and datetime would be work. (Basically just use a valid date format and it works).

### Updating api and models
- An Api cannot be updated if it already has models associated to it.
- A model cannot be updated if it already has entries/data in it.
- A model field constraints cannot be removed, it can only be appended to. (This would be improved in further versions)

### Deleting api and models
- You can delete apis and models if not needed anymore
- If you delete an api all the models associated would be automatically deleted
- Remember when deleting an api or model that is a foreign key of another model you won't be able to access the foreign key anymore
    - Regarding this feature there would be improvement in the future versions where there would be an `on-delete` feature on the model that would define the behavior when a foreign key is deleted.
    - The current behavior of this is that models that there would be 2 scenarios (already created, being created)
        - If a model is referencing the deleted model and already has fields that it is pointing to e.g in a blog api you have a reference to the user model `{Author: '1'...}` if you delete the user model the Author field would retain its values and not set to null (This would be improved in future versions) you would have to manually set this.
        - If a model is being created and the foreign key is still pointing to an already deleted model, it won't be created it would throw an error and prevent the entry from being created, the work around to this is to add the `nullable` constraints to the foreign key field if you have no intention of using it anymore(as there is no feature to delete fields yet) or you can update the **Foreign Key Reference Table** to point to another `api.table` and then go ahead to update

    - **Note** You can only set a foreign key field to `null` only if there is a `nullable` constraints set(you can always update the field to append the nullable constraints).



## Contributors
* **Peter Erinfolami**
    * **Github** (https://github.com/shady-cj)
    * **Linkedin** www.linkedin.com/in/erinfolamipeter/
    * **Email** petersp2000@gmail.com
    * **Twitter** https://twitter.com/shady_cj

* **Kehinde Owolabi**
    * **Github** https://github.com/owolabi250
    * **Linkedin** https://www.linkedin.com/in/owolabi-kehinde-37b448151/
    * **Email** owolabikehinde250@gmail.com
    * **Twitter** https://twitter.com/Elder_Choco

* **Kenneth Igbo**
    * **Github** https://github.com/CodeRaiden
    * **Linkedin** https://www.linkedin.com/in/kenneth-igbo-b26bb5208/
    * **Email** Hadoken10@yahoo.com
    * **Twitter** https://twitter.com/KenRaiden7

## Contribute

Like **DummyApi Builder**? Thanks!!!

At the same time, we need your help

## Finding Bugs

DummyApi is just getting started. If you could help us find or fix potential bugs, we would be grateful!

Have a bug or a feature request? [Please open a new issue](https://github.com/shady-cj/dummy_api_builder/issues)

## New Features

Have some awesome ideas? Feel free to open an issue or submit your pull request directly!

## Documentation improvements.

Improvements to README and documentation are welcome at all times, whether typos or our lame English. 🤣.

