# skincare-price-prediction

This project aims to predict the prices of skincare products using machine learning, enhanced with MLOps practices for robust, automated, and scalable workflows.

## 📌 Overview

Skincare products vary significantly in price depending on brand, ingredients, type, and other features. This project scrapes real-world data from online beauty platforms like Purplle or Nykaa, trains regression models to predict prices based on product features, and deploys the model with a CI/CD-enabled MLOps pipeline.

---

## 🧠 Machine Learning Pipeline

1. **Data Collection**  
   - Web scraping using `Selenium`  
   - Extract product names, prices, ratings, reviews, specifications, brand info,Skin Type and Country of Origin

2. **Data Preprocessing**  
   - Handle missing data  
   - Clean textual and categorical features  
   - Encode and normalize 

3. **Model Training**  
   - Regression models: `LinearRegression`, `RandomForestRegressor`, `XGBoost`  
   - Evaluation using RMSE, MAE, and R² metrics

4. **Model Tracking**  
   - Versioning & tracking with **MLflow**

5. **Deployment**  
   - Model served via `FastAPI` or `Flask`  
   - CI/CD with GitHub Actions  
   - Dockerized and optionally deployed to platforms like **Heroku**, **AWS**, or **GCP**

---

## 🔧 Tech Stack

| Component        | Tool/Library            |
|------------------|-------------------------|
| Web Scraping     | Selenium, BeautifulSoup |
| Data Analysis    | Pandas, NumPy           |
| ML Models        | Scikit-learn, XGBoost   |
| Experiment Tracking | MLflow               |
| Model Deployment | FastAPI/Flask + Docker  |
| CI/CD            | GitHub Actions          |
| Visualization    | Matplotlib, Seaborn     |

---

## 📊 Example Features Used

-   Price
-   Original Price
-   Rating
-   Reviews
-   Skin Type
-   Country of Origin

---


### Clone this repo

```bash
git clone https://github.com/your-username/skincare-price-prediction-mlops.git
cd skincare-price-prediction-mlops
