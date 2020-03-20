The goal of this assignment is to implement RESTful API webservice that will be responsible for
managing and storing in database simple notes (without the UI part). For solution use
tech/framework of your choice.
1. Webservice has to accept HTTP calls for creating, reading, updating and deleting notes
(CRUD).
2. Notes has to contain fields:
    a. Title - string (required)
    b. Content - string (required)
    c. Created - date of initial creation
    d. Modified - date of last modification
3. Created/Modified date fields should be read-only and filled automatically by webservice
4. Webservice should validate if required fields are filled and return apropriate HTTP error
status if input data is invalid.
5. Notes should be versioned, which means that on each note update, new instance of the
note should be created with incremental version number, so that whole history of
changes of particular note can be traced. By default webservice should return only the
latest version of the note.
6. There should be an additional webservice that will return whole history of changes for
particular note.
7. Deleted notes should also be stored in the database, so that they are not taken into
account by “get all” or “get by id” webservices, but visible for the version history
webservice from previous point.
8. For purpose of this assignment ignore the authorization and authentication aspect.
9. You can use any database of your choice.
10. Use library of your choice to create integration tests for each functionality. Running tests
should use in-memory database.
11. Project should contain README.md file with description:
    a. What is required for running the project
    b. Steps how to run scripts that will setup database for the project
    c. Steps how to build and run the project
    d. Example usages (ie. like example curl commands)