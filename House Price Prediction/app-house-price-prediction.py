import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import sklearn.datasets
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

app = Flask(__name__, template_folder='templates')

# Load and prepare the dataset
house_price_dataset = sklearn.datasets.fetch_california_housing()
house_price_dataframe = pd.DataFrame(house_price_dataset.data, columns=house_price_dataset.feature_names)
house_price_dataframe['price'] = house_price_dataset.target

X = house_price_dataframe.drop(['price'], axis=1)
Y = house_price_dataframe['price']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Train the model
model = XGBRegressor()
model.fit(X_train, Y_train)

# Evaluate the model
test_data_prediction = model.predict(X_test)
score_1 = metrics.r2_score(Y_test, test_data_prediction)
score_2 = metrics.mean_absolute_error(Y_test, test_data_prediction)
print('R Squared Error:', score_1)
print('Mean Absolute Error:', score_2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input features from the form
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]

    # Make the prediction
    prediction = model.predict(final_features)

    # Format the output
    output = round(prediction[0] * 100000, 4)  # Multiply by 100,000 and round to 4 decimal places

    # Return the prediction to the user
    return render_template('index.html', prediction_text='Estimated House Price: ${:,.4f}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)