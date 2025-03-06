from flask import Flask, request, jsonify
import os
from serverless_wsgi import handle_request

application = handle_request(app)from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("https://lpbdbsngdvwcshxyjfwp.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwYmRic25nZHZ3Y3NoeHlqZndwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyMzU3ODcsImV4cCI6MjA1NjgxMTc4N30.IrsreKxnAfgpqD6A5Hftcc9K1-XD217WLJqbtK8-xqY")

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    target = data.get("query")
    return jsonify({"message": f"Searching for {target}..."})

if __name__ == "__main__":
    app.run(debug=True)

import whois

def domain_lookup(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date)
        }
    except:
        return {"error": "Domain lookup failed"}

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get("query")

    result = {}

    if "@" in query:
        result["email_breach"] = search_email_breach(query)
    elif "." in query:
        result["domain_info"] = domain_lookup(query)

    return jsonify(result)
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_search(query, result):
    supabase.table("search_logs").insert({"query": query, "result": result}).execute()
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def calculate_risk_score(breach_count, domain_age):
    # Normalize data to a 0-100 scale
    scaler = MinMaxScaler(feature_range=(0, 100))
    data = np.array([[breach_count, domain_age]])
    return scaler.fit_transform(data)[0][0]

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get("query")
    breach_count = len(search_email_breach(query)) if "@" in query else 0
    domain_age = 2025 - int(domain_lookup(query)["creation_date"][:4]) if "." in query else 0

    risk_score = calculate_risk_score(breach_count, domain_age)

    return jsonify({
        "query": query,
        "breach_count": breach_count,
        "domain_age": domain_age,
        "risk_score": round(risk_score, 2)
    })
