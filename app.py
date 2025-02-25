from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

app = Flask(__name__)

# List of Locations and Patient Names
locations = [
    "Temeke", "Kinondoni", "Kigamboni", "Jangwani", "Sinza", "Ubungo", "Mbezi", "Kimara", 
    "Mbagala", "Chamanzi", "Keko", "Mtoni", "Kongowe", "Kibada", "Chang'ombe", "Kisutu", 
    "Ukonga", "Kitunda"
]
names = [
    "John Doe", "Jane Smith", "Samuel Lee", "Alex Green", "Mary Blue", "David Brown", 
    "Emma White", "Oliver Black", "Sophia Gray", "Liam Red", "Noah Silver", "Ava Gold",
    "Isabella Copper", "Elijah Bronze", "Mia Emerald", "Ethan Jade", "Amelia Pearl"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    location_filter = request.args.get('location', default=None)

    if request.method == 'POST' or location_filter:
        num_records = 1000
        diseases = ["Diabetes", "Hypertension", "Asthma", "Tuberculosis", "Malaria", "Influenza", "HIV/AIDS", "Dengue", "Cholera", "Pneumonia"]
        symptoms = ["Fever", "Cough", "Shortness of Breath", "Fatigue", "Headache", "Sweating", "Chest Pain", "Nausea", "Vomiting", "Diarrhea"]
        treatment_methods = ["Antibiotics", "Antivirals", "Vaccination", "Oxygen Therapy", "Pain Relievers", "IV Fluids", "Insulin", "Dialysis"]
        diagnostic_tools = ["X-ray", "MRI", "Blood Test", "PCR Test", "Urinalysis", "ECG", "CT Scan", "Ultrasound"]

        ages = np.random.randint(1, 100, num_records)
        smoking_habits = np.random.choice([0, 1], num_records)
        water_quality = np.random.choice(["Clean", "Contaminated"], num_records)
        transport_crowding = np.random.choice(["Low", "Moderate", "High"], num_records)
        weather_conditions = np.random.choice(["Hot", "Cold", "Moderate"], num_records)
        waste_disposal = np.random.choice(["Safe", "Unsafe"], num_records)

        assigned_diseases = np.random.choice(diseases, num_records)
        assigned_symptoms = [", ".join(np.random.choice(symptoms, np.random.randint(2, 5))) for _ in range(num_records)]
        assigned_treatments = [", ".join(np.random.choice(treatment_methods, np.random.randint(1, 3))) for _ in range(num_records)]
        assigned_diagnostics = [", ".join(np.random.choice(diagnostic_tools, np.random.randint(1, 3))) for _ in range(num_records)]
        assigned_locations = np.random.choice(locations, num_records)
        assigned_names = np.random.choice(names, num_records)

        # Create DataFrame
        df = pd.DataFrame({
            "Patient Name": assigned_names,
            "Location": assigned_locations,
            "Age": ages,
            "Disease": assigned_diseases,
            "Symptoms": assigned_symptoms,
            "Treatment": assigned_treatments,
            "Diagnosis": assigned_diagnostics,
            "Smoker": smoking_habits,
            "Water Quality": water_quality,
            "Transport Crowding": transport_crowding,
            "Weather": weather_conditions,
            "Waste Disposal": waste_disposal
        })

        # Filter by location if specified
        if location_filter:
            df = df[df['Location'] == location_filter]

        # Define age intervals
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
        df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

        # Convert categorical columns to numerical for clustering
        df_encoded = df.copy()
        df_encoded["Water Quality"] = df_encoded["Water Quality"].map({"Clean": 0, "Contaminated": 1})
        df_encoded["Transport Crowding"] = df_encoded["Transport Crowding"].map({"Low": 0, "Moderate": 1, "High": 2})
        df_encoded["Weather"] = df_encoded["Weather"].map({"Cold": 0, "Moderate": 1, "Hot": 2})
        df_encoded["Waste Disposal"] = df_encoded["Waste Disposal"].map({"Safe": 0, "Unsafe": 1})

        # Standardize numerical features
        scaler = StandardScaler()
        numerical_features = ["Age", "Smoker", "Water Quality", "Transport Crowding", "Weather", "Waste Disposal"]
        df_encoded[numerical_features] = scaler.fit_transform(df_encoded[numerical_features])

        # Apply KMeans clustering for diseases and treatments
        kmeans_disease = KMeans(n_clusters=4, random_state=42, n_init=10)
        df_encoded["Disease Cluster"] = kmeans_disease.fit_predict(df_encoded[numerical_features])

        kmeans_treatment = KMeans(n_clusters=4, random_state=42, n_init=10)
        df_encoded["Treatment Cluster"] = kmeans_treatment.fit_predict(df_encoded[numerical_features])

        # Group by Disease Cluster and Treatment Cluster
        disease_cluster_groups = df_encoded.groupby('Disease Cluster').apply(lambda group: group.drop('Disease Cluster', axis=1).to_html(classes='table table-striped'))
        treatment_cluster_groups = df_encoded.groupby('Treatment Cluster').apply(lambda group: group.drop('Treatment Cluster', axis=1).to_html(classes='table table-striped'))

        # Train predictive model
        X = df_encoded[numerical_features]
        y = df["Disease"].astype("category").cat.codes  

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_test)
        classification_rep = classification_report(y_test, y_pred, output_dict=True)

        # Convert classification report to DataFrame
        report_df = pd.DataFrame(classification_rep).transpose()

        # Pass all results to the template
        return render_template("results.html", tables=[df.head().to_html(classes='table table-striped table-bordered table-hover'),
                                                       df_encoded.head().to_html(classes='table table-striped able-bordered table-hover'),
                                                       report_df.to_html(classes='table table-striped')],
                               disease_cluster_groups=disease_cluster_groups.to_dict(),
                               treatment_cluster_groups=treatment_cluster_groups.to_dict(),
                               age_groups=df["Age Group"].value_counts().sort_index().to_dict(),
                               locations=locations, location_filter=location_filter)

    return render_template('index.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
