from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)

app.secret_key = "customer_segmentation_secret"

UPLOAD_FOLDER = "uploads"
PLOT_FOLDER = "static/plots"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)


# --------------------------------------------------
# GLOBAL DATA STORAGE
# --------------------------------------------------

customer_data = None
segmented_data = None
cluster_summary = None
cluster_insights = None
optimal_k = None
silhouette = None


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# FIND COLUMN HELPER
# --------------------------------------------------

def find_column(data, possible_names):

    for column in data.columns:

        normalized_column = (
            column.lower()
            .replace("_", " ")
            .replace("(", "")
            .replace(")", "")
            .replace("$", "")
            .replace("-", " ")
            .strip()
        )

        for name in possible_names:

            normalized_name = (
                name.lower()
                .replace("_", " ")
                .replace("(", "")
                .replace(")", "")
                .replace("$", "")
                .replace("-", " ")
                .strip()
            )

            # Exact match
            if normalized_name == normalized_column:

                return column

            # Partial match
            if normalized_name in normalized_column:

                return column

    return None


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if segmented_data is None:

        return render_template(
            "dashboard.html",
            total_customers=0,
            clusters=0,
            avg_income=0,
            avg_spending=0,
            has_data=False
        )

    income_col = find_column(
        segmented_data,
        [
            "annual income",
            "income",
            "annual_income"
        ]
    )

    spending_col = find_column(
        segmented_data,
        [
            "spending score",
            "spending_score",
            "spending"
        ]
    )

    avg_income = (
        round(segmented_data[income_col].mean(), 2)
        if income_col else 0
    )

    avg_spending = (
        round(segmented_data[spending_col].mean(), 2)
        if spending_col else 0
    )

    return render_template(
        "dashboard.html",
        total_customers=len(segmented_data),
        clusters=optimal_k,
        avg_income=avg_income,
        avg_spending=avg_spending,
        has_data=True,
        silhouette=silhouette
    )


# --------------------------------------------------
# UPLOAD DATASET
# --------------------------------------------------

@app.route("/upload", methods=["GET", "POST"])
def upload():

    global customer_data

    if request.method == "POST":

        file = request.files.get("dataset")

        if not file or file.filename == "":

            flash(
                "Please select a CSV file.",
                "error"
            )

            return redirect(
                url_for("upload")
            )

        if not file.filename.lower().endswith(".csv"):

            flash(
                "Only CSV files are supported.",
                "error"
            )

            return redirect(
                url_for("upload")
            )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        try:

            customer_data = pd.read_csv(
                filepath
            )

            flash(
                f"Dataset uploaded successfully! "
                f"{len(customer_data)} records loaded.",
                "success"
            )

            return redirect(
                url_for("segmentation")
            )

        except Exception as e:

            flash(
                f"Error reading dataset: {str(e)}",
                "error"
            )

            return redirect(
                url_for("upload")
            )

    return render_template(
        "upload.html"
    )


# --------------------------------------------------
# CUSTOMER SEGMENTATION
# --------------------------------------------------

@app.route("/segmentation", methods=["GET", "POST"])
def segmentation():

    global segmented_data
    global cluster_summary
    global cluster_insights
    global optimal_k
    global silhouette

    if customer_data is None:

        flash(
            "Please upload a dataset first.",
            "error"
        )

        return redirect(
            url_for("upload")
        )

    # --------------------------------------------------
    # RUN SEGMENTATION
    # --------------------------------------------------

    if request.method == "POST":

        # Select numerical columns
        numeric_columns = (
            customer_data
            .select_dtypes(include=np.number)
            .columns
            .tolist()
        )

        # Remove ID columns
        feature_columns = [

            col

            for col in numeric_columns

            if "id" not in col.lower()

        ]

        if len(feature_columns) < 2:

            flash(
                "Dataset must contain at least "
                "two numerical features.",
                "error"
            )

            return redirect(
                url_for("segmentation")
            )

        # --------------------------------------------------
        # PREPARE DATA
        # --------------------------------------------------

        data = customer_data.copy()

        data = data.dropna(
            subset=feature_columns
        )

        X = data[
            feature_columns
        ]

        # --------------------------------------------------
        # FEATURE SCALING
        # --------------------------------------------------

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(
            X
        )

        # --------------------------------------------------
        # FIND OPTIMAL K
        # --------------------------------------------------

        best_score = -1
        best_k = 2

        max_k = min(
            8,
            len(X_scaled) - 1
        )

        for k in range(
            2,
            max_k + 1
        ):

            model = KMeans(

                n_clusters=k,

                random_state=42,

                n_init=10

            )

            labels = model.fit_predict(
                X_scaled
            )

            score = silhouette_score(
                X_scaled,
                labels
            )

            if score > best_score:

                best_score = score

                best_k = k

        # --------------------------------------------------
        # FINAL K-MEANS MODEL
        # --------------------------------------------------

        kmeans = KMeans(

            n_clusters=best_k,

            random_state=42,

            n_init=10

        )

        data["Cluster"] = (
            kmeans.fit_predict(
                X_scaled
            )
        )

        segmented_data = data

        optimal_k = best_k

        silhouette = round(
            best_score,
            3
        )

        # --------------------------------------------------
        # CLUSTER SUMMARY
        # --------------------------------------------------

        cluster_summary = (

            segmented_data

            .groupby("Cluster")[feature_columns]

            .mean()

            .round(2)

            .reset_index()

            .to_dict(
                orient="records"
            )

        )

        # --------------------------------------------------
        # AUTOMATIC CLUSTER INSIGHTS
        # --------------------------------------------------

        income_col = find_column(

            segmented_data,

            [
                "annual income",
                "income"
            ]

        )

        spending_col = find_column(

            segmented_data,

            [
                "spending score",
                "spending"
            ]

        )

        cluster_insights = []

        # Generate insights only when
        # income and spending columns exist

        if income_col and spending_col:

            overall_income = (
                segmented_data[
                    income_col
                ].mean()
            )

            overall_spending = (
                segmented_data[
                    spending_col
                ].mean()
            )

            for cluster in range(best_k):

                cluster_data = (

                    segmented_data[
                        segmented_data[
                            "Cluster"
                        ] == cluster
                    ]

                )

                avg_income = (

                    cluster_data[
                        income_col
                    ].mean()

                )

                avg_spending = (

                    cluster_data[
                        spending_col
                    ].mean()

                )

                # ------------------------------------------
                # HIGH INCOME + HIGH SPENDING
                # ------------------------------------------

                if (

                    avg_income >= overall_income

                    and

                    avg_spending >= overall_spending

                ):

                    name = (
                        "High-Value Customers"
                    )

                    description = (

                        "Customers with strong purchasing "
                        "power and high spending behavior."

                    )

                # ------------------------------------------
                # LOW INCOME + LOW SPENDING
                # ------------------------------------------

                elif (

                    avg_income < overall_income

                    and

                    avg_spending < overall_spending

                ):

                    name = (
                        "Budget Customers"
                    )

                    description = (

                        "Customers with lower income and "
                        "lower spending behavior."

                    )

                # ------------------------------------------
                # HIGH INCOME + LOW SPENDING
                # ------------------------------------------

                elif (

                    avg_income >= overall_income

                    and

                    avg_spending < overall_spending

                ):

                    name = (
                        "High Income, Low Spending"
                    )

                    description = (

                        "Customers with strong purchasing "
                        "power but relatively lower spending."

                    )

                # ------------------------------------------
                # LOW INCOME + HIGH SPENDING
                # ------------------------------------------

                else:

                    name = (
                        "Low Income, High Spending"
                    )

                    description = (

                        "Customers with lower income but "
                        "higher spending behavior."

                    )

                cluster_insights.append({

                    "cluster": cluster,

                    "name": name,

                    "description": description,

                    "customers": len(
                        cluster_data
                    ),

                    "avg_income": round(
                        avg_income,
                        2
                    ),

                    "avg_spending": round(
                        avg_spending,
                        2
                    )

                })

        # --------------------------------------------------
        # GENERATE VISUALIZATIONS
        # --------------------------------------------------

        generate_plots(

            segmented_data,

            feature_columns,

            X_scaled

        )

        flash(

            "Customer segmentation completed successfully!",

            "success"

        )

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------------------
    # SEGMENTATION PAGE
    # --------------------------------------------------

    numeric_columns = (

        customer_data

        .select_dtypes(
            include=np.number
        )

        .columns

        .tolist()

    )

    feature_columns = [

        col

        for col in numeric_columns

        if "id" not in col.lower()

    ]

    return render_template(

        "segmentation.html",

        columns=feature_columns

    )


# --------------------------------------------------
# GENERATE VISUALIZATIONS
# --------------------------------------------------

def generate_plots(
    data,
    features,
    X_scaled
):

    # --------------------------------------------------
    # CLUSTER DISTRIBUTION
    # --------------------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    sns.countplot(

        data=data,

        x="Cluster"

    )

    plt.title(
        "Customer Distribution by Cluster"
    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PLOT_FOLDER,

            "cluster_distribution.png"

        )

    )

    plt.close()


    # --------------------------------------------------
    # CUSTOMER CLUSTER SCATTER PLOT
    # --------------------------------------------------

    if len(features) >= 2:

        plt.figure(
            figsize=(8, 6)
        )

        sns.scatterplot(

            data=data,

            x=features[0],

            y=features[1],

            hue="Cluster",

            palette="viridis",

            s=80

        )

        plt.title(
            "Customer Segmentation Visualization"
        )

        plt.tight_layout()

        plt.savefig(

            os.path.join(

                PLOT_FOLDER,

                "customer_clusters.png"

            )

        )

        plt.close()


    # --------------------------------------------------
    # ELBOW METHOD
    # --------------------------------------------------

    inertias = []

    max_k = min(
        8,
        len(X_scaled)
    )

    for k in range(
        1,
        max_k + 1
    ):

        model = KMeans(

            n_clusters=k,

            random_state=42,

            n_init=10

        )

        model.fit(
            X_scaled
        )

        inertias.append(
            model.inertia_
        )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(

        range(
            1,
            max_k + 1
        ),

        inertias,

        marker="o"

    )

    plt.xlabel(
        "Number of Clusters (K)"
    )

    plt.ylabel(
        "WCSS"
    )

    plt.title(
        "Elbow Method"
    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PLOT_FOLDER,

            "elbow_method.png"

        )

    )

    plt.close()


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

@app.route("/analytics")
def analytics():

    if segmented_data is None:

        flash(

            "Please run customer segmentation first.",

            "error"

        )

        return redirect(
            url_for("segmentation")
        )

    return render_template(

        "analytics.html",

        cluster_summary=cluster_summary,

        cluster_insights=cluster_insights,

        optimal_k=optimal_k,

        silhouette=silhouette

    )


# --------------------------------------------------
# DOWNLOAD SEGMENTED DATASET
# --------------------------------------------------

@app.route("/download-results")
def download_results():

    if segmented_data is None:

        flash(

            "Please run customer segmentation first.",

            "error"

        )

        return redirect(
            url_for("segmentation")
        )

    output_path = os.path.join(

        UPLOAD_FOLDER,

        "segmented_customer_data.csv"

    )

    segmented_data.to_csv(

        output_path,

        index=False

    )

    return send_file(

        output_path,

        as_attachment=True,

        download_name=(
            "segmented_customer_data.csv"
        )

    )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )