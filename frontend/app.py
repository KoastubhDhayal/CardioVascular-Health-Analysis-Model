from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vaish',
            database='sleepData'
        )
        if connection.is_connected():
            print("Database connection successful.")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search-user', methods=["GET", "POST"])
def search_user():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        if not user_id:
            flash("User ID is required.", "error")
            return render_template("search_user.html")
        
        return redirect(url_for('view_user_details', user_id=user_id))

    return render_template("search_user.html")

@app.route('/view-user-details/<int:user_id>')
def view_user_details(user_id):
    connection = get_db_connection()
    if connection is None:
        return render_template("error.html", message="Database connection failed.")

    user_details = None
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Cardio WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_details = cursor.fetchone()

        if not user_details:
            return render_template("error.html", message="User not found.")

        return render_template("view_user_details.html", user=user_details)

    except Error as e:
        print(f"Error: {e}")
        return render_template("error.html", message="An error occurred while fetching data.")

    finally:
        if cursor:
            try:
                cursor.close()
            except Error as e:
                print(f"Cursor close error: {e}")
        if connection:
            try:
                connection.close()
            except Error as e:
                print(f"Connection close error: {e}")

@app.route('/calculate_risk', methods=['GET', 'POST'])
def calculate_risk():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        
        if not user_id:
            return render_template("calculate_risk.html", error="User ID is required.")

        connection = get_db_connection()
        if connection is None:
            return render_template("error.html", message="Database connection failed.")
        
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT cardio_impact FROM Cardio WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            
            if result is None:
                return "User not found", 404

            # Convert cardio_impact to float
            cardio_impact = float(result['cardio_impact'])

            # Determine health status based on the cardio_impact score
            if 80 <= cardio_impact <= 100:
                health_status = "Excellent Cardiovascular Health"
            elif 60 <= cardio_impact < 80:
                health_status = "Good Cardiovascular Health"
            elif 40 <= cardio_impact < 60:
                health_status = "Moderate Cardiovascular Health"
            elif 20 <= cardio_impact < 40:
                health_status = "Poor Cardiovascular Health"
            else:
                health_status = "Very Poor Cardiovascular Health"

            return render_template("results.html", cardio_impact=cardio_impact, health_status=health_status)
        
        except Error as e:
            print(f"Error: {e}")
            return render_template("error.html", message="An error occurred while fetching data.")
        
        finally:
            if cursor:
                try:
                    cursor.close()
                except Error as e:
                    print(f"Cursor close error: {e}")
            if connection:
                try:
                    connection.close()
                except Error as e:
                    print(f"Connection close error: {e}")

    return render_template("calculate_risk.html")

if __name__ == '__main__':
    app.run(debug=True)
