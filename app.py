from flask import *
from google import genai
import mysql.connector as my
import hashlib

app = Flask(__name__)

# Connect to MySQL database
pwrd = "krish113838G"


try:
    mycon = my.connect(host='localhost',
                       user='root',
                       password=pwrd)

except:
    print("Wrong password!")
    exit(0)

if not mycon.is_connected():
    print("Not able to connect to the server at this movement")
    exit(0)
    
else:
    print("Connected")

cr = mycon.cursor()
cr.execute("CREATE DATABASE IF NOT EXISTS AIVersus")
cr.execute("USE AIVersus")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register_page():
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login_page():
    return render_template("login.html")


@app.route("/query", methods=["POST"])
def query_page():
    qry = request.form.get("Query")
    print("\n\n", qry, "\n\n")
    client = genai.Client(api_key="AIzaSyDLtRhhQTS05XcusmCaYX0m-NHEJK_Wq88")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[qry]
    )
    print("\n\n", response.text, "\n\n")
    # print("\n\n", response, "\n\n")
    
    return{"response": response.text}
    
    # return {"response": response.results[0].content}
    # return {"response": qry} 
    
    
    
    
    
@app.route("/registerit", methods=["POST"])
def registerit():
    # Get form data
    password = request.form.get("password")
    emailId = request.form.get("email")
    name = request.form.get("name")

    # Validate inputs
    if not password or password.isspace():
        return jsonify({"status": "error", "message": "Password cannot be empty or whitespace"}), 400
    elif len(password) < 8:
        return jsonify({"status": "error", "message": "Password must be at least 8 characters long"}), 400
    elif not password.isalnum():
        return jsonify({"status": "error", "message": "Password must be alphanumeric"}), 400

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print("Hashed password: ", hashed_password)

    # Validate email and name
    if not emailId or not name:
        return jsonify({"status": "error", "message": "Email and Name cannot be empty"}), 400

    try:
        # Create the table if it doesn't exist
        cr.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                name VARCHAR(200), 
                email VARCHAR(500), 
                password VARCHAR(10240),
                PRIMARY KEY (email)
            )
            """
        )

        # Use parameterized query to insert data
        query = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
        values = (name, emailId, hashed_password)
        cr.execute(query, values)

        # Commit the transaction to save changes
        mycon.commit()

        print("User registered successfully!")
        return jsonify({"status": "success", "message": "User registered successfully!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": "An error occurred while registering the user"}), 500
    

    
    

    
    

if __name__ == "__main__":
    app.run(debug=True)
