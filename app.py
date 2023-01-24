from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/smartphones')
def smartphones():
    with open('smartphones.json') as f:
        data = json.load(f)

    price = request.args.get('price')

    if price:
        filtered_data = [item for item in data if item['price'] == int(price)]
        if filtered_data:
            return jsonify(filtered_data)
        else:
            return jsonify({'message': 'No smartphones found with the specified price'}), 404
    else:
        return jsonify({'message': 'Price parameter is missing'}), 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
