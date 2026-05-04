from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

import os
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route('/research', methods=['POST'])
def research_lead():
    data = request.json
    name = data.get('name', '')
    company = data.get('company', '')
    role = data.get('role', '')
    
    # Search for lead info
    search_query = f"{name} {role} {company}"
    
    tavily_response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": search_query,
            "search_depth": "basic",
            "max_results": 3
        }
    )
    
    search_results = tavily_response.json()
    results_text = "\n".join([r['content'] for r in search_results.get('results', [])])
    
    return jsonify({
        "research": results_text,
        "status": "success"
    })


app.run(port=8080, debug=True)