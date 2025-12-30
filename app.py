from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
chain = Blockchain(difficulty=4)

@app.get("/chain")
def get_chain():
    return jsonify({"length": len(chain.chain), "valid": chain.is_valid(), "chain": chain.to_list()})

@app.post("/mine")
def mine():
    payload = request.get_json(silent=True) or {}
    data = payload.get("data", {"note": "empty"})
    block = chain.add_block(data)
    return jsonify({"mined": block.__dict__})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
