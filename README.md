# WebChatify

This repository contains the source code for a chat web server implemented using Django and websockets.

## Description

The chat web server allows users to communicate with each other in real-time using websockets. It provides the following features:

- User authentication and password management
- User registration if the username doesn't exist in the database
- User login with password verification
- User logout with appropriate notifications in the chat
- Unique color assignment to each user's nickname for the current session
- Ability for users to create their own chat rooms
- Other users can join chat rooms only by invitation
- User information for each chat room is stored in the database using a one-to-many relationship

## Installation

To run this project locally, you need to have Python and Django installed. You can install the required dependencies by running the following command:

```sh
pip install -r requirements.txt
```

The project also requires Redis server. You can run a Redis server using Docker by executing the following command:

```docker
docker run -p 6379:6379 -d redis:5
```

## Usage

To start the chat web server, run the following command:

```sh
python manage.py runserver
```


Once the server is running, you can access the chat application in your web browser.



