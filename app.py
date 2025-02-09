from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import scipy.stats as stats

app = Flask(__name__)

# Real-world health dataset: Comparing treatment methods and patient recovery rates
#data = {
    #'Treatment Method': ['A']*10 + ['B']*10 + ['C']*10,
   # 'Recovery Rate (%)': [65, 70, 68, 75, 72, 74, 78, 71, 69, 73, 80, 85, 82, 88, 90, 87, 83, 86, 84, 89, 55, 60, 58, 62, 59, 57, 61, 63, 56, 54]
#}
#df = pd.DataFrame(data)
df = pd.read_csv('dataset.csv')

# Group the data by Treatment Method
grouped = [df[df['Treatment Method'] == method]['Recovery Rate (%)'] for method in ['A', 'B', 'C']]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Perform the ANOVA test
    f_statistic, p_value = stats.f_oneway(*grouped)
    
    # Round the f_statistic to 2 decimal places
    f_statistic = round(f_statistic, 2)
    
    # Store the original p_value (as a float) for comparison purposes
    original_p_value = p_value
    
    # Format p_value for display (show scientific notation for very small p-values)
    if p_value < 0.01:
        p_value_display = f"{p_value:.2e}"  # Scientific notation for p-values < 0.01
    else:
        p_value_display = f"{p_value:.2f}"  # Regular formatting for larger p-values
    
    # Set the alpha value for hypothesis testing
    alpha = 0.05
    
    # Compare the original p_value (not the formatted string) with alpha
    if original_p_value < alpha:
        result = "Reject the null hypothesis. There is a significant difference in recovery rates among treatment methods."
    else:
        result = "Fail to reject the null hypothesis. No significant difference in recovery rates among treatment methods."

    # Prepare methods data for rendering in the template
    methods_data = {
        'A': df[df['Treatment Method'] == 'A'],
        'B': df[df['Treatment Method'] == 'B'],
        'C': df[df['Treatment Method'] == 'C']
    }

    # Return the template with the required variables
    return render_template('index.html', f_statistic=f_statistic, p_value=p_value_display, result=result, methods_data=methods_data)




@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
