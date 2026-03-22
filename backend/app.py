from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load ML Model
# -----------------------------
model = pickle.load(open("../models/purchase_model.pkl", "rb"))
churn_model = pickle.load(open("../models/churn_model.pkl", "rb"))
# -----------------------------
# Database connection
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# API: Get Customers
# -----------------------------
@app.route('/get_customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])
# -----------------------------
# API: Get Orders
# -----------------------------
@app.route('/get_orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM customers LIMIT 50").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

# -----------------------------
# 🤖 API: Predict Purchase
# -----------------------------
@app.route('/predict_purchase', methods=['POST'])
def predict_purchase():
    data = request.get_json()

    try:
        # Extract input
        recency = data['Recency']
        frequency = data['Frequency']
        monetary = data['Monetary']
        avg_order_value = data['Avg_Order_Value']

        # Convert to numpy array
        features = np.array([[recency, frequency, monetary, avg_order_value]])
        # Prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        # Save prediction to DB
        conn = get_db_connection()

        conn.execute("""
        INSERT INTO predictions (Recency, Frequency, Monetary, Avg_Order_Value, Purchase_Prediction)
        VALUES (?, ?, ?, ?, ?)
        """, (recency, frequency, monetary, avg_order_value, int(prediction)))

        conn.commit()
        conn.close()

        return jsonify({
            "prediction": int(prediction),
            "probability": float(probability),
            "message": "Customer will likely buy again"
                       if prediction == 1 else
                       "Customer may not buy again"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
# -----------------------------
# 🤖 API: Predict Churn
# -----------------------------
@app.route('/predict_churn', methods=['POST'])
def predict_churn():
    data = request.get_json()

    try:
        # Extract input
        recency = data['Recency']
        frequency = data['Frequency']
        monetary = data['Monetary']
        avg_order_value = data['Avg_Order_Value']

        #Prepare input
        features = np.array([[recency, frequency, monetary, avg_order_value]])
        # Prediction
        prediction = churn_model.predict(features)[0]
        probability = churn_model.predict_proba(features)[0][1]

        conn = get_db_connection()

        conn.execute("""
        INSERT INTO predictions (Recency, Frequency, Monetary, Avg_Order_Value, Churn_Prediction)
        VALUES (?, ?, ?, ?, ?)
        """, (recency, frequency, monetary, avg_order_value, int(prediction)))

        conn.commit()
        conn.close()    

        return jsonify({
            "prediction": int(prediction),
            "probability": float(probability),
            "message": "Customer is likely to churn"
                       if prediction == 1 else
                       "Customer is active"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
# -----------------------------
# 🤖 API: Segmentation API
# -----------------------------
@app.route('/get_segments', methods=['GET'])
def get_segments():
    conn = get_db_connection()
    
    data = conn.execute("""
        SELECT Customer_ID, Recency, Frequency, Monetary, Cluster, Customer_Segment
        FROM customers
        LIMIT 50
    """).fetchall()
    
    conn.close()

    return jsonify([dict(row) for row in data])

#API for Power
@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM predictions").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)