API: http://127.0.0.1:8000/profile/create/ - Creates new user account

Method: POST
Takes: 
{
    "username": "<email or username>",
    "password": "<password>",
}

Response:

New user created: Status code 201
{
    "username": "aquaware1@test.bg"
}


If user already exists: Status code 400
{
    "username": [
        "A user with that username already exists."
    ]
}


API: http://127.0.0.1:8000/profile/login/ Login user

Method: POST
Takes: 
{
    "username": "<email or username>",
    "password": "<password>",
}


Response:

User successfully logged in: Status code 200
{
    "token": "f3768e6996f537b0168cd82c8c22edd557548317",
    "user_id": 7
}

If login failed: Status code 400
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}


API: http://127.0.0.1:8000/profile/details/<int:user_id>/ Profile details

Method: GET
Takes: 
No data

Response:

{
    "first_name": null,
    "last_name": null,
    "email": "",
    "client_number": "",
    "phone_number": null,
    "date_joined": "2024-05-17T09:31:41.411095Z",
    "profile_picture": null
}

Method: PUT
Takes: 
{
    "first_name": "Firstname",
    "last_name": "Lastname",
    "email": "email@email.com",
    "client_number": "123123",
    "phone_number": "0123456789",
    "date_joined": "2024-05-17T09:31:41.411095Z",
    "profile_picture": <file upload>
}


Response:

Profile successfully updated: Status code 200


Method: DELETE
Takes: 
No data


Response:

Profile successfully deleted: Status code 200



Admin credentials for the Django admin panel: http://127.0.0.1:8000/admin/
user: aquaware_admin
pass: admin123