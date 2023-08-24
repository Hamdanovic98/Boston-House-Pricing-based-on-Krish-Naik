import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('regmodel.pkl', 'rb'))
scalar = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')
# Read the housing.csv data
column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'Price']
data = pd.read_csv('housing.csv', header=None, delimiter=r"\s+", names=column_names)


# Convert the DataFrame to JSON format
data_json = data.to_json(orient='records')

# If you want to save the JSON data to a file
with open("housing.json", "w") as json_file:
    json_file.write(data_json)

@app.route('/predict_api', methods=['POST'])
def predict_api():
    # Get the incoming data from POST request
    incoming_data = request.json
    
    # Convert the dictionary to a DataFrame
    new_data_df = pd.DataFrame([incoming_data])
    
    # Transform the new data
    scaled_data = scalar.transform(new_data_df)
    
    # Predict using the regression model
    output = model.predict(scaled_data)
    
    # Ensure the output is a single number
    if isinstance(output[0], (float, int)):
        return jsonify(float(output[0]))
    else:
        return jsonify({"error": "Unexpected prediction output."})

if __name__ == "__main__":
    app.run(debug=True)
