from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_connection():
    """Create and return a new database connection using environment variables.

    Expected environment variables (set these in Render and locally):
    - DB_HOST
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
    - DB_PORT (optional, defaults to 5432)
    """

    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", "5432"),
        sslmode="require",
    )

@app.route('/api/iot', methods=['POST'])
def receive_data():
    try:
        data = request.json
        print("Incoming:", data)

        email = data.get("email")
        moisture = data.get("moisture")
        ph = data.get("ph")
        temperature = data.get("temperature")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sensor_data (email, moisture, ph, temperature)
            VALUES (%s, %s, %s, %s)
        """, (email, moisture, ph, temperature))

        conn.commit()
        cur.close()
        conn.close()   # 🔥 VERY IMPORTANT

        return jsonify({"status": "success"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
if __name__ == "__main__":
    # Render provides PORT as an environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)