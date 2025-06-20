from flask import Flask, render_template, request, jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))                         

@app.route('/', methods= ['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''    
    poutcome = 0
    if request.method == 'POST':
        duration = float(request.form['Duration'])
        
        poutcome = request.form['Previous Outcome']
        if(poutcome == 'Success'):
            poutcome_success = 1
            poutcome_other = 0
            poutcome_unknown = 0
        elif(poutcome == 'Other'):
            poutcome_success = 0
            poutcome_other = 1
            poutcome_unknown = 0       
        elif(poutcome == 'Unkownn'):
            poutcome_success = 0
            poutcome_other = 0
            poutcome_unknown = 1
        else:
            poutcome_success = 0
            poutcome_other = 0
            poutcome_unknown = 0
        
        contacted_before = request.form['Contacted Before']
        if(contacted_before == 'Yes'):
            contacted_before_yes = 1
        else:
            contacted_before_yes = 0

        month = request.form['Month']
        if(month == 'March'):
            month_mar = 1
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 0
        elif(month == 'October'):
            month_mar = 0
            month_oct = 1
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 0
        elif(month == 'September'):
            month_mar = 0
            month_oct = 0
            month_sep = 1
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 0
        elif(month == 'Decmeber'):
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 1
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 0
        elif(month == 'Febuary'):
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 1
            month_jun = 0
            month_jul = 0
            month_may = 0
        elif(month == 'June'):
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 1
            month_jul = 0
            month_may = 0
        elif(month == 'July'):
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 1
            month_may = 0
        elif(month == 'May'):
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 1
        else:
            month_mar = 0
            month_oct = 0
            month_sep = 0
            month_dec = 0
            month_feb = 0
            month_jun = 0
            month_jul = 0
            month_may = 0

        previous = int(request.form['Previous'])

        job = request.form['Job']
        if(job == 'Retired'):
            job_retired = 1
            job_student = 0
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 0
        elif(job == 'Student'):
            job_retired = 0
            job_student = 1
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 0        
        elif(job == 'Management'):
            job_retired = 0
            job_student = 0
            job_management = 1
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 0
        elif(job == 'Unemployed'):
            job_retired = 0
            job_student = 0
            job_management = 0
            job_unemployed  = 1
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 0 
        elif(job == 'Entrepreneur'):
            job_retired = 0
            job_student = 0
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 1
            job_services = 0
            job_blue_collar = 0 
        elif(job == 'Services'):
            job_retired = 0
            job_student = 0
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 1
            job_blue_collar = 0
        elif(job == 'Blue Collar'):
            job_retired = 0
            job_student = 0
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 1
        else:
            job_retired = 0
            job_student = 0
            job_management = 0
            job_unemployed  = 0
            job_entrepreneur = 0
            job_services = 0
            job_blue_collar = 0

        marital = request.form['Marital Status']
        if(marital == 'Single'):
            marital_single = 1
            marital_married = 0
        elif(marital == 'Married'):
            marital_single = 0
            marital_married = 1
        else:
            marital_single = 0
            marital_married = 0

        balance = float(request.form['Balance'])        
        age = int(request.form['Age'])

        contact = request.form['Contact Medium']
        if(contact == 'Telephone'):
            contact_telephone = 1
            contact_unknown = 0
        elif(contact == 'Unknown'):
            contact_telephone = 0
            contact_unknown = 1
        else:
            contact_telephone = 0
            contact_unknown = 0

        education = request.form['Education Level']
        if(education == 'Tertiary'):
            education_tertiary = 1
            education_secondary = 0
        elif(education == 'Secondary'):
            education_tertiary = 0
            education_secondary = 1
        else:
            education_tertiary = 0
            education_secondary = 0

        default = request.form['Default']
        if(default == 'Yes'):
            default_yes = 1
        else:
            default_yes = 0

        loan = request.form['Loan']
        if(loan == 'Yes'):
            loan_yes = 1
        else:
            loan_yes = 0

        campaign = int(request.form['Campaign'])

        housing = request.form['Housing']
        if(housing == 'Yes'):
            housing_yes = 1
        else:
            housing_yes = 0

        prediction=model.predict([[duration,
                                 poutcome_success,
                                 contacted_before_yes,
                                 previous,
                                 month_oct, 
                                 month_sep, 
                                 month_mar, 
                                 education_tertiary,
                                 job_retired,
                                 marital_single, 
                                 job_student, 
                                 month_dec,
                                 balance, 
                                 month_feb, 
                                 poutcome_other, 
                                 job_management,
                                 age,
                                 job_unemployed, 
                                 contact_telephone, 
                                 job_entrepreneur,
                                 month_jun, 
                                 job_services, 
                                 default_yes, 
                                 month_jul,
                                 education_secondary, 
                                 marital_married, 
                                 loan_yes,
                                 job_blue_collar, 
                                 campaign, 
                                 month_may, 
                                 housing_yes,
                                 poutcome_unknown, 
                                 contact_unknown
                                ]])
                                
        if prediction[0] == 1:
            text = "The Client is Likely to Subscribe to a Term Deposit"
        else:
            text = "The Client is Unlikely to Subscribe to a Term Deposit"

        return render_template('index.html',prediction_text=text)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
