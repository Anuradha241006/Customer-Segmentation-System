🎯 CUSTOMER SEGMENTATION SYSTEM

A professional Machine Learning-based web application that analyzes customer data and groups customers into different segments based on their similarities, characteristics, and behavior.

The project performs data preprocessing, feature selection, data scaling, K-Means clustering, cluster evaluation using Silhouette Score, Exploratory Data Analysis, customer segmentation, data visualization, and interactive analytics through a Flask web application.

📌 Project Overview

Customer Segmentation System is a Machine Learning-based web application developed to group customers into different segments based on their similarities and characteristics.

Customer segmentation helps businesses understand their customers better by identifying groups of customers with similar behavior and characteristics. This information can be useful for improving marketing strategies, customer service, and business decision-making.

The system uses the K-Means Clustering algorithm to group similar customers into different clusters.

🎯 Objectives

📊 Analyze customer data.
👥 Identify similar groups of customers.
🤖 Perform customer segmentation using Machine Learning.
🧠 Apply the K-Means Clustering algorithm.
🔍 Determine a suitable number of clusters.
📈 Visualize customer segments.
💡 Provide useful insights for business decision-making.

🛠️ Technologies Used

💻 Programming Language

Python

🌐 Web Framework

Flask

🤖 Machine Learning
Scikit-learn
K-Means Clustering
StandardScaler
Silhouette Score
📊 Data Analysis
Pandas
NumPy
📈 Data Visualization
Matplotlib
Seaborn
🎨 Frontend Technologies
HTML
CSS
JavaScript

📁 Project Structure

Customer-Segmentation-System/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── customer_data.csv
│   └── processed/
│       └── processed_customer_data.csv
│
├── models/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── plots/
│       ├── cluster_distribution.png
│       ├── customer_clusters.png
│       └── elbow_method.png
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── segmentation.html
│   ├── analytics.html
│   └── dashboard.html
│
└── uploads/
    ├── customer_segmentation_dataset.csv
    └── segmented_customer_data.csv

⚙️ Working Process

📥 Data Collection

Customer data is provided to the system in CSV format.

🧹 Data Preprocessing

The dataset is cleaned and prepared for analysis.

🔢 Feature Selection

Relevant numerical features are selected for customer segmentation. Customer ID and other identifier columns are excluded from the clustering process.

⚖️ Data Scaling

The selected features are scaled using StandardScaler. This helps ensure that differences in feature value ranges do not negatively affect the clustering process.

🔍 Finding the Best Number of Clusters

Different cluster values are tested, and the Silhouette Score is used to evaluate the quality of clustering.

🤖 K-Means Clustering

The K-Means algorithm groups customers with similar characteristics into different clusters.

📊 Result Visualization

The clustering results and customer segments are displayed using graphs and visualizations.

✨ Features

📊 Customer data analysis
🧹 Data preprocessing
🔢 Numerical feature selection
⚖️ Data scaling using StandardScaler
🤖 Customer segmentation using K-Means Clustering
📈 Cluster evaluation using Silhouette Score
📉 Customer segment visualization
💡 Business insights
🖥️ User-friendly web interface

🎯 Applications

The Customer Segmentation System can be used for:

📢 Targeted marketing
👥 Customer behavior analysis
🎁 Personalized recommendations
🤝 Customer relationship management
📈 Business strategy development
🔍 Identifying different customer groups

🚀 Installation and Setup

1️⃣ Download the Project

Clone or download the project.

2️⃣ Open the Project Folder

Open the Customer Segmentation System project folder.

3️⃣ Create Virtual Environment

Create and activate a Python virtual environment.

4️⃣ Install Required Libraries

Install all required libraries using the requirements.txt file.

5️⃣ Run the Application

Run:

python app.py
6️⃣ Open in Browser

Open:

http://127.0.0.1:5000/

🔮 Future Enhancements

🤖 Add more clustering algorithms.
📊 Compare multiple clustering techniques.
🖥️ Add an interactive dashboard.
🗄️ Store customer data in a database.
🔐 Add user authentication.
📄 Generate downloadable reports.
☁️ Deploy the application online.

👩‍💻 Author

Anuradha Bayana

B.Tech – Artificial Intelligence and Data Science

👥 Customer Segmentation System
Built with Python, Machine Learning, K-Means Clustering, Flask, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, HTML, CSS, JavaScript, and GitHub.
