
import pymongo
import pandas as pd
from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["Patients"]

app = Flask(__name__)

account_sid = 'AC557a16dc5303f912724783187944b126'
auth_token = '3152ab05dcc0b5ad7e6e33206eea610c'
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visitWindow')
def visitWindow():
    return render_template('visitWindow.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/register', methods=['POST'])
def Register():
    if request.method == 'POST':
   
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        age = request.form['age']
        address = request.form['address']
        mobile1 = request.form['mobile1']
        mobile2 = request.form['mobile2']
        gender = request.form['gender']  
        disease = request.form['disease']  
        blood_group = request.form['blood_group']  
        insurance_option = request.form['insurance_option']  

    
        data = {
            "FirstName": firstname,
            "MiddleName": middlename,
            "LastName": lastname,
            "Age": age,
            "Address": address,
            "Mobile1": mobile1,
            "Mobile2": mobile2,
            "Gender": gender,
            "Disease": disease,
            "BloodGroup": blood_group,
            "InsuranceOption": insurance_option
        }
 
        pdf_file_path, blood_group_display = generate_pdf(firstname, middlename, lastname, age, address, mobile1, mobile2, gender, disease, blood_group, insurance_option)
        
 
        message = client.messages.create(
            from_='+15707540743',
            body=f'Patient name: {data["FirstName"]} {data["MiddleName"]} {data["LastName"]} \nAge: {data["Age"]} \nMobile Number 1: {data["Mobile1"]} \nMobile Number 2: {data["Mobile2"]} \nGender: {data["Gender"]} \nDisease: {data["Disease"]} \nBlood Group: {blood_group_display} \nInsurance: {data["InsuranceOption"]}',
            to='+918849577787'
        )

        print(message.sid)
        return render_template('Register.html', pdf_file=pdf_file_path)

def generate_pdf(firstname, middlename, lastname, age, address, mobile1, mobile2, gender, disease, blood_group, insurance_option):

    blood_group_mapping = {
        "ap": "A+",
        "bp": "B+",
        "abp": "AB+",
        "op": "O+",
        "on": "O-",
        "abn": "AB-",
        "bn": "B-",
        "an": "A-"
    }

    blood_group_display = blood_group_mapping.get(blood_group, blood_group)
    data1 = {
            "FirstName": firstname,
            "MiddleName": middlename,
            "LastName": lastname,
            "Age": age,
            "Address": address,
            "Mobile1": mobile1,
            "Mobile2": mobile2,
            "Gender": gender,
            "Disease": disease,
            "BloodGroup": blood_group,
            "InsuranceOption": insurance_option
        }
    mycol.insert_one(data1)
    pdf_file_path = f"{firstname}.pdf"
    p = canvas.Canvas(pdf_file_path, pagesize=letter)
    p.setFont("Helvetica",31)
    p.drawString(155,730 ,"Narayan Health Care")
    
    p.setFont("Helvetica", 27)
    p.drawString(175,670, "Registration Details")
    p.setFont("Helvetica", 20)
    p.drawString(100, 610, f"First Name: {firstname}")
    p.drawString(100, 570, f"Middle Name: {middlename}")
    p.drawString(100, 530, f"Last Name: {lastname}")
    p.drawString(100, 490, f"Age: {age}")
    p.drawString(100, 450, f"Address: {address}")
    p.drawString(100, 410, f"Mobile 1: {mobile1}")
    p.drawString(100, 370, f"Mobile 2: {mobile2}")
    p.drawString(100, 330, f"Gender: {gender}")
    p.drawString(100, 290, f"Disease: {disease}")
    p.drawString(100, 250, f"Blood Group: {blood_group_display}") 
    p.drawString(100, 210, f"Insurance Option: {insurance_option}")
    
    p.save()
    
    return pdf_file_path, blood_group_display
    


@app.route('/download_registration_confirmation/<filename>')
def download_registration_confirmation(filename):
    return send_file(filename, as_attachment=True)

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

if __name__ == '__main__':
    app.run(debug=True)
