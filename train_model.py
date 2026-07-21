import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
#Load dataset
print ("Loading dataset...")
df = pd.read_csv("used_cars.csv")
print(df.head())
#check missing values
print("\nMissing values")
print(df.isnull().sum())
df=df

categorical_columns = [
"Brand",
"Fuel",
"Transmission",
"Owner"
]
label_encoders ={}
for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    label_encoders[column]=encoder
print("\nCategorical Encoding Completed")
#features and target
X = df.drop("Price",axis=1)
y = df["Price"]
#train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
print("\nTraining Samples :",len(X_train))
print("Testing Samples :",len(X_test))
# Train random forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
print("\nTRaining Model...")
model.fit(X_train, y_train)
print("Training completed")
#prediction
Y_pred = model.predict(X_test)
#evaluation
mae = mean_absolute_error(y_test, Y_pred)
mse = mean_squared_error(y_test, Y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, Y_pred)
print("\n==================")
print("Model Performance")
print("=====================")
print(f"MAE :{mae:.2f}")
print(f"MSE : {mse:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2 Score : {r2:.4f}")
#save model 
with open("car_price_model.pkl", "wb") as file:
    pickle.dump(model, file)
print("\nMOdel Saved : car_price_model.pkl")
#save label encoders
with open("label_encoders.pkl", "wb") as file:
    pickle.dump(label_encoders, file)
    print ("Label Encoders Saved : label_encoders.pkl")
    #feature importance
    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance":model.feature_importances_
})
    importance = importance.sort_values(
        by="Importance",
        ascending=False
)
    print("\nFeature Importance")
    print(importance)
    print("\n==============================")
    print("Training Completed Successfully")
    print("=================================")
