from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import joblib
import os
import pandas as pd

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import (
    create_tables,
    save_disease_prediction,
    save_yield_prediction,
    get_disease_history,
    get_yield_history,
    get_connection
)

from ml.predict import predict_disease
from weather_api import get_weather


app = Flask(__name__)

app.secret_key = "smart-agriculture-secret-key"

app.config["UPLOAD_FOLDER"] = "static/uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

create_tables()


# ==========================================
# LOAD YIELD MODEL
# ==========================================

yield_model = joblib.load("model/yield_model.pkl")


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = None

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except Exception:

            conn.close()

            message = "Email already registered."

    return render_template(
        "register.html",
        message=message
    )


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect(url_for("dashboard"))

        else:

            message = "Invalid email or password."

    return render_template(
        "login.html",
        message=message
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================================
# DISEASE DETECTION
# ==========================================

@app.route("/disease", methods=["GET", "POST"])
def disease():

    disease_name = None
    confidence = None

    if request.method == "POST":

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image.save(image_path)

            disease_name, confidence = predict_disease(
                image_path
            )

            save_disease_prediction(
                disease=disease_name,
                confidence=confidence,
                image=filename,
                user_id=session.get("user_id")
            )

    return render_template(
        "disease.html",
        disease=disease_name,
        confidence=confidence
    )


# ==========================================
# WEATHER PAGE
# ==========================================

@app.route("/weather")
def weather():

    try:

        latitude = 21.1458
        longitude = 79.0882

        weather_data = get_weather(
            latitude,
            longitude
        )

        return render_template(
            "weather.html",
            weather=weather_data
        )

    except Exception as e:

        return render_template(
            "weather.html",
            weather=None,
            error=str(e)
        )


# ==========================================
# WEATHER API
# ==========================================

@app.route("/api/weather")
def api_weather():

    try:

        latitude = 21.1458
        longitude = 79.0882

        weather_data = get_weather(
            latitude,
            longitude
        )

        return jsonify(weather_data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# YIELD PREDICTION
# ==========================================

@app.route("/yield", methods=["GET", "POST"])
def yield_prediction():

    if request.method == "POST":

        crop = request.form["crop"]

        area = float(
            request.form["area"]
        )

        rainfall = float(
            request.form["rainfall"]
        )

        temperature = float(
            request.form["temperature"]
        )

        humidity = float(
            request.form["humidity"]
        )

        soil_ph = float(
            request.form["soil_ph"]
        )

        fertilizer = float(
            request.form["fertilizer"]
        )

        data = pd.DataFrame([
            {
                "Crop": crop,
                "Area": area,
                "Rainfall": rainfall,
                "Temperature": temperature,
                "Humidity": humidity,
                "Soil_pH": soil_ph,
                "Fertilizer": fertilizer
            }
        ])

        prediction = float(
            yield_model.predict(data)[0]
        )

        save_yield_prediction(

            crop=crop,

            area=area,

            rainfall=rainfall,

            temperature=temperature,

            humidity=humidity,

            soil_ph=soil_ph,

            fertilizer=fertilizer,

            predicted_yield=prediction,

            user_id=session.get("user_id")
        )

        return render_template(

            "result.html",

            prediction=f"{prediction:.2f}",

            crop=crop,

            area=area,

            rainfall=rainfall,

            temperature=temperature,

            humidity=humidity,

            soil_ph=soil_ph,

            fertilizer=fertilizer

        )

    return render_template(
        "yield.html",
        prediction=None
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    disease_history = get_disease_history()

    yield_history = get_yield_history()

    return render_template(

        "dashboard.html",

        disease_history=disease_history,

        yield_history=yield_history

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )