"""Main module."""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/fund/<str:fund_id>', methods=['GET'])
def get_fund_by_id(fund_id: str):

    pass


# driver function
if __name__ == '__main__':
    app.run(debug=True)
