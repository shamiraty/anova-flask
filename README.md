# MACHINE LEARNING & SCIENTIFIC RESEARCH USING PROGRAMMING LANGUAGES

# ONE-WAY ANOVA TEST FOR HEALTH DATA ANALYSIS*

# One-Way ANOVA Analysis Documentation

<img src="https://github.com/user-attachments/assets/90e6bb44-455c-4079-9a4d-59feadce6fdb" alt="logo7" width="100" height="100" />

- **Location**: Dodoma, Tanzania
- **Email**: [sashashamsia@gmail.com](mailto:sashashamsia@gmail.com)
- **WhatsApp**: [+255675839840](https://wa.me/255675839840)
- **Demo**: [Online](https://anova.pythonanywhere.com/)
  <!--- **Youtube**: [Videos](https://www.youtube.com/channel/UCjepDdFYKzVHFiOhsiVVffQ)-->

| Icon | Rank | Professional Target Audience                                |
|------|------|------------------------------------------------------------|
| 🔬  | 1    | Healthcare Researchers (Epidemiologists, Clinical Researchers) |
| 🩺  | 2    | Physicians (General Practitioners and Specialists)            |
| 🏛️  | 3    | Public Health Officials (Health Department Personnel, Policy Makers) |
| 🏢  | 4    | Hospital Administrators                                      |
| 👩‍⚕️ | 5    | Nurses                                                     |
| 📊  | 6    | Data Analysts in Healthcare                                   |
| 👨‍💼 | 7    | Medical Directors                                          |
| 💊  | 8    | Pharmacists                                                 |
| 🏥  | 9    | Clinic Administrators                                        |
| 🎓  | 10   | Medical Educators (Professors of medicine)                   |

## Disclaimer

> The patient records used to train and test the **Symptom-Matcher AI** model are **not real patient data**. They are **fictitious data** that have been generated for educational purposes only. These records have no connection to any actual individuals or real-life medical conditions. 

> The diseases and symptoms displayed in the application are **for learning and demonstration purposes**. They do not represent actual medical diagnoses and should not be interpreted as such. The use of these simulated cases is intended solely for academic and training purposes.

> This application and its content are not intended to diminish or disrespect the real-world medical field, institutions, or individuals. The information presented is purely hypothetical and should not be used for making medical decisions. The primary goal of this project is to provide a platform for learning and development in the field of machine learning and healthcare technology.

## Introduction
This project is a Flask-based web application that performs a One-Way ANOVA analysis on a real-world health dataset. The dataset compares different treatment methods and their respective patient recovery rates. The application reads the dataset, processes the data, and performs a statistical test to determine if there are significant differences in recovery rates among treatment methods.

## Features
- Upload and process a dataset containing treatment methods and recovery rates.
- Perform a One-Way ANOVA test to compare treatment effectiveness.
- Display statistical results including F-statistic and p-value.
- Provide a visual and interactive user interface using Bootstrap and DataTables.

## Technologies Used
- Python (Flask, Pandas, NumPy, SciPy)
- HTML, CSS (Bootstrap for styling)
- JavaScript (jQuery, DataTables for interactive tables)

## Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/anova-analysis.git

# Navigate to the project directory
cd anova-analysis

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

## Flask Application Structure
```
anova-analysis/
│-- static/
│   ├── css/
│   │   ├── style.css
│-- templates/
│   ├── index.html
│   ├── tutorials.html
│-- dataset.csv
│-- app.py
│-- requirements.txt
│-- README.md
```

## Flask Routes
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Performs the ANOVA test and renders the results on the homepage.
    """
    f_statistic, p_value = stats.f_oneway(*grouped)
    p_value_display = f"{p_value:.2e}" if p_value < 0.01 else f"{p_value:.2f}"
    alpha = 0.05
    result = "Reject the null hypothesis." if p_value < alpha else "Fail to reject the null hypothesis."
    return render_template('index.html', f_statistic=f_statistic, p_value=p_value_display, result=result, methods_data=methods_data)
```

## ANOVA Statistical Analysis
```python
import pandas as pd
import numpy as np
import scipy.stats as stats

df = pd.read_csv('dataset.csv')
grouped = [df[df['Treatment Method'] == method]['Recovery Rate (%)'] for method in ['A', 'B', 'C']]

# Perform ANOVA test
f_statistic, p_value = stats.f_oneway(*grouped)
print(f"F-Statistic: {f_statistic:.2f}, P-Value: {p_value:.4f}")
```

## Frontend (HTML, CSS, JS)
### Bootstrap and DataTables Integration
```html
<!-- DataTables Initialization -->
<script>
    $(document).ready(function() {
        $('#anovaTable').DataTable();
    });
</script>
```

## Results Interpretation
- **F-Statistic**: Measures variance between treatment groups. A higher value suggests a greater difference.
- **P-Value**: If p < 0.05, reject the null hypothesis, indicating a significant difference in recovery rates.

## Future Enhancements
- Extend analysis to include post-hoc tests.
- Implement data visualization (e.g., Matplotlib, Seaborn charts).
- Allow users to upload custom datasets.

## License
This project is open source

## Contact
For questions or contributions, contact via WhatsApp: [Click Here](https://wa.me/+255675839840)
