# RESTful_API

<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div class="jumbotron">
        <div class="col-sm-8 mx-auto">
          <p>Implementation of a RESTful API webservice responsible for managing and storing in database simple notes, the implementation does not contain UI part.</p>
          <p>The webservice accepts HTTP calls for creating, reading, updating and deleting notes (CRUD)</p> 
          <p>The notes consist of the fields:</p>         
            <ul>
                <li>Title - string</li>
                <li>Content - string</li>
                <li>Created - date of initial creation</li>
                <li>Modified - date of last modification</li>
            </ul>
            <p>The history of changes and deletion is kept for all the notes</p>
            <hr>
          <h2>How to execute:</h2>
          <h3>Download required files:</h3>
          <code>git clone https://github.com/cridav/RESTful_API.git</code>
          <br>
          <code>cd RESTful_API/</code>
          <br>
          <h3>Setup the database:</h3>
          <code>python</code>
          <br>
          <code>>>> from restful_api import db</code>
          <br>
          <code>>>> db.create_all()</code>
          <br>
          <code>>>> exit()</code>
          <br>
          <h3>Run the project:</h3>
          <code>python restful_api.py</code>
          <h3>Example usages:</h3>
          <h4>POST</h4>
          <code>curl -X POST -d '{"title":"title_sample_1","content":"content_sample_1"}' http://127.0.0.1:5000/notes</code>
          <hr>
          <h4>GET all notes</h4>
          <code>curl -X GET http://127.0.0.1:5000/notes</code>
          <hr>
          <h4>GET by ID <small>for instance, ID=1:</small></h4>          
          <code>curl -X GET http://127.0.0.1:5000/notes/1</code>
          <hr>
          <h4>UPDATE by ID</h4>
          <small>The entry should be in JSON format, and the ID must be specified; modifying the first entry (ID=1):</small>
          <br>
          <code>curl -X PUT -d '{"title":"title_sample_1_modified","content":"content_sample_1_modified"}' http://127.0.0.1:5000/notes/1</code>
          <hr>
          <h4>DELETE by ID <small>deleting note with ID=1</small></h4>
          <code>curl -X DELETE http://127.0.0.1:5000/notes/1</code>
          <hr>
          <h4>GET all records</h4>
          <code>curl -X GET  http://127.0.0.1:5000/record</code>
          <hr>
          <h4>GET all records by ID <small>for instance, all the records for the note with ID=1</small></h4>
          <code>curl -X GET  http://127.0.0.1:5000/record/1</code>
          <br>
          <p>
          </p>
        </div>
      </div>
</body>
</html>