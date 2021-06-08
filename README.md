# Notif.ai recruitment task

The application is an API for saving, returning saved and edit short texts (up to 160 characters). App is written in the FastAPI Framework
 
The application should be available at https://daftcode-course.herokuapp.com/

Automatic documentation provided by the FastAPI framework is available at https://daftcode-course.herokuapp.com/docs#/

A few words about endpoints and how they work:
## /get_text/{id} metoda: GET
endpoint for getting texts with user-specified ID, available to users of all users (authorized and unauthorized)
returns objeect in format:
```
{
    'id': int
    'visit_counter': int
    'text': str
}
```

## /put_text metoda: POST 
endpoint used to create or edit (if the user gives an ID that already exists, the object will be edited)
texts with the given ID, requires authorization. Requires a json file in the format:
```
{
    'id': int
    'text': str
}
```
## /delete_text/{id} metoda: DELETE
endpoint used to remove texts with the given ID, requires authorization.

## /login metoda: GET
endopoint for authorization, the user will be able to use the POST and DELETE methods

## /get_text metoda: GET
endpoint returns all Text objects and their IDs from the database

the application has been deployed using herok according to the instructions in the link https://github.com/daftcode/daftacademy-python_levelup-spring2021/blob/master/1_D_jak_deploy/D_jak_Deploy.ipynb points 5 and 6
