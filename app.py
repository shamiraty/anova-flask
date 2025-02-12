from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go

app = Flask(__name__)

# Real-world health dataset
# Real-world health dataset: Comparing treatment methods and patient recovery rates
data = {
    'Treatment Method': ['A']*10 + ['B']*10 + ['C']*10,
    'Recovery Rate (%)': [65, 70, 68, 75, 72, 74, 78, 71, 69, 73, 80, 85, 82, 88, 90, 87, 83, 86, 84, 89, 55, 60, 58, 62, 59, 57, 61, 63, 56, 54]
}
df = pd.DataFrame(data)
#df = pd.read_csv('dataset.csv')

# Group the data by Treatment Method
grouped = [df[df['Treatment Method'] == method]['Recovery Rate (%)'] for method in ['A', 'B', 'C']]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Perform the ANOVA test
    f_statistic, p_value = stats.f_oneway(*grouped)

    f_statistic = round(f_statistic, 2)
    original_p_value = p_value

    if p_value < 0.01:
        p_value_display = f"{p_value:.2e}"
    else:
        p_value_display = f"{p_value:.2f}"

    alpha = 0.05

    if original_p_value < alpha:
        result = "Reject the null hypothesis. There is a significant difference in recovery rates among treatment methods."
    else:
        result = "Fail to reject the null hypothesis. No significant difference in recovery rates among treatment methods."

    methods_data = {
        'A': df[df['Treatment Method'] == 'A'],
        'B': df[df['Treatment Method'] == 'B'],
        'C': df[df['Treatment Method'] == 'C']
    }

     # Calculate means for each group
    means = {method: round(data['Recovery Rate (%)'].mean(), 2) for method, data in methods_data.items()}

    # Calculate the overall mean
    overall_mean = round(df['Recovery Rate (%)'].mean(), 2)

    # Calculate the percentage of overall mean
    mean_percentages = {method: round((mean / overall_mean) * 100, 2) for method, mean in means.items()}

    return render_template(
        'index.html',
        f_statistic=f_statistic,
        p_value=p_value_display,
        result=result,
        methods_data=methods_data,
        means=means,
        overall_mean=overall_mean,
        mean_percentages=mean_percentages
    )


@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')

@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)