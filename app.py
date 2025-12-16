from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import random
import secrets
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

ASSIGNMENTS_FILE = 'secret_santa_assignments.xlsx'

# Load employee data
def load_employees():
    data = {
        'Full Name': ['Sharath Nag Rahula', 'viswanth', 'Sowmya Mamanduru', 'Sreedhar Konety', 
                      'Jagadeesh Reddy Katamareddy', 'Srinivas Konatham', 'Srilaxmi Seelam', 
                      'Gopi Sandhireddy', 'Paidi Madhuri', 'Sai Kiran Kesi', 'KAVYASRI BOMMAKANTI', 
                      'Rawaly Marla', 'Rahul Bhati', 'Amruta Pramod Desai', 'Nageswara Ramavath', 
                      'Maruthi Telaprolu', 'Satya Venkat Chintalapudi', 'Santosh Reddy Gottam', 
                      'Tarun Kumar Reddy Chelimilla', 'Ashish Kumar', 'Mahesh Gantepaka', 
                      'Charan Tej Reddy Pagidela', 'Usha S', 'Yashwanth Manne', 'AMULYA GUNDRATHI', 
                      'Shivanand Ramachandra Futane', 'Ramesh Boda', 'Harshitha Manne', 
                      'BHAROTHU NIHIL NAIK', 'Hamsalekha Nomula', 'NIHARIKA GATTU', 'Srilakshmi Koneru', 
                      'Karthik Reddy Alagoti', 'Venkata Lakshmi Prasanna Manda', 'Sreekanth Uppari', 
                      'Bhawna Tickoo', 'KARNING NARESH GOUD', 'Mukund Pokala', 'Anvitha Gaddampalli', 
                      'Alekhya Gayam', 'Leela Renuka Devi Adapa', 'Nihar Ranjan Samantray', 
                      'Navinash Gummadavalli', 'Praveen Kumar Dama', 'Sumitha Cunchan', 
                      'Venkata Appala Nagesh Potula', 'Akhil Yadav Manne', 'HARENDRA SINGH', 
                      'Mahesh Gaddameeda', 'Sai Akhil Siddi', 'Rajasekar Reddy Alimili', 
                      'Hemanth Kumar Reddy Peddamunthala', 'Rahul Chowdary Katragadda', 
                      'Venakata Ramana Mekala Mekala', 'Srimayee Kurimilla', 'Eshaan Sangyam', 
                      'Yeshwanth Reddy Sarikuti', 'Sri Vidya Reddy Nagam', 'Karthik Pandla', 
                      'Pushyami Bommareddy', 'Ashritha Varla', 'Vijay Vardhan Chimmula', 
                      'Roja Reddy Mamidala', 'Tejaswini Khilare', 'Himasri Katamareddy', 'Naveen P', 
                      'Vishwanath Tallavajhulla', 'Vinay Kumar Reddy M', 'Fahad Badri', 
                      'Rakesh Reddy Kakanuru', 'Datta D Holkar', 'Bikash Barik', 'Renju Sreerag', 
                      'Manisha Kayasth', 'Chandrasekhar Chinthapatla', 'Eti Gautam', 'Amulya Muthoju', 
                      'Sowmya Nagam', 'Hemanth Chikballapur'],
        'Email': ['sharath.rahula@letitbexai.com', 'viswanatha@letitbexai.com', 'sowmya.m@letitbexai.com', 
                  'sreedhar.konety@letitbexai.com', 'jagadeesh@letitbexai.com', 'srinivas.konatham@letitbexai.com', 
                  'sri.laxmi@letitbexai.com', 'gopi.sandhireddy@letitbexai.com', 'madhuri.paidi@letitbexai.com', 
                  'saikiran.kesi@letitbexai.com', 'kavyasri.vasala@letitbexai.com', 'rawaly.marla@letitbexai.com', 
                  'rahul.bhati@letitbexai.com', 'amruta.desai@letitbexai.com', 'nageswara.ramavath@letitbexai.com', 
                  'maruthirao.telaprolu@letitbexai.com', 'satyavenkat.chintalapudi@letitbexai.com', 
                  'santhoshreddy.gottam@letitbexai.com', 'tarunkumar.chelimilla@letitbexai.com', 
                  'ashish.kumar@letitbexai.com', 'mahesh.gantepaka@letitbexai.com', 
                  'charantej.pagidela@letitbexai.com', 'usha.s@letitbexai.com', 'yashwanth.manne@letitbexai.com', 
                  'amulya.gundrathi@letitbexai.com', 'shivanand.ramachandra@letitbexai.com', 
                  'ramesh.boda@letitbexai.com', 'harshitha.manne@letitbexai.com', 'nikhilbharothu@letitbexai.com', 
                  'hamsalekha.nomula@letitbexai.com', 'niharika.gattu@letitbexai.com', 
                  'srilakshmi.koneru@letitbexai.com', 'karthik.alagoti@letitbexai.com', 
                  'manda.lakshmiprasanna@letitbexai.com', 'sreekanth.uppari@letitbexai.com', 
                  'bhawana.tickoo@letitbexai.com', 'naresh.goud@letitbexai.com', 'mk@letitbexai.com', 
                  'anvitha.gaddampalli@letitbexai.com', 'alekhya.gayam@letitbexai.com', 
                  'leela.adapa@letitbexai.com', 'nihar.ranjan@letitbexai.com', 'navinash.g@letitbexai.com', 
                  'praveen.dama@letitbexai.com', 'sumitha.cunchan@letitbexai.com', 'nagesh.pothula@letitbexai.com', 
                  'akhil.manne@letitbexai.com', 'harendra.singh@letitbexai.com', 'mahesh.gaddameeda@letitbexai.com', 
                  'akhil.siddi@letitbexai.com', 'rajasekar.alimili@letitbexai.com', 
                  'hemanth.peddamunthala@letitbexai.com', 'rahul.ck@letitbexai.com', 
                  'venkataramana.mekala@letitbexai.com', 'srimayee.kurimilla@letitbexai.com', 
                  'eshaan.sangyam@letitbexai.com', 'yeshwanth.sarikuti@letitbexai.com', 
                  'nagamsrividyareddy@gmail.com', 'karthik.pandla@letitbexai.com', 
                  'pushyami.bommareddy@letitbexai.com', 'ashritha.varla@letitbexai.com', 
                  'vijay.vardhanreddy@letitbexai.com', 'rojareddy.mamidala@letitbexai.com', 
                  'tejaswini.khilare@letitbexai.com', 'himasri.k@letitbexai.com', 'naveen.p@letitbexai.com', 
                  'vishwanath.tallavajhulla@letitbexai.com', 'vinaykumar.reddy@letitbexai.com', 
                  'fahaad.badri@letitbexai.com', 'rakeshreddy.k@letitbexai.com', 'datta.holkar@letitbexai.com', 
                  'bikash.barik@letitbexai.com', 'renju.sreerag@letitbexai.com', 'manisha.kayasth@letitbexai.com', 
                  'chandrasekhar.chinthapatla@letitbexai.com', 'eti@letitbexai.com', 'amulya.muthoju@letitbexai.com', 
                  'nagam.sowmya@letitbexai.com', 'hemanth.chikballapur@letitbexai.com']
    }
    return pd.DataFrame(data)

def load_assignments():
    if os.path.exists(ASSIGNMENTS_FILE):
        return pd.read_excel(ASSIGNMENTS_FILE)
    return pd.DataFrame(columns=['Email', 'Name', 'Assigned_To', 'Timestamp'])

def save_assignment(email, name, assigned_to):
    df = load_assignments()
    new_row = pd.DataFrame({
        'Email': [email],
        'Name': [name],
        'Assigned_To': [assigned_to],
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(ASSIGNMENTS_FILE, index=False)

employees_df = load_employees()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveal')
def reveal():
    return render_template('reveal.html')

@app.route('/verify_email', methods=['POST'])
def verify_email():
    email = request.json.get('email', '').strip().lower()
    
    # Check if email exists
    if email not in employees_df['Email'].str.lower().values:
        return jsonify({'success': False, 'message': 'Email not found in the list'})
    
    # Check if already used
    assignments_df = load_assignments()
    if email in assignments_df['Email'].str.lower().values:
        return jsonify({'success': False, 'message': 'You have already participated'})
    
    # Get person's name
    person_name = employees_df[employees_df['Email'].str.lower() == email]['Full Name'].values[0]
    
    # Store in session
    session['email'] = email
    session['name'] = person_name
    
    return jsonify({'success': True})

@app.route('/get_numbers', methods=['GET'])
def get_numbers():
    if 'email' not in session:
        return jsonify({'success': False, 'message': 'Session expired'})
    
    email = session['email']
    person_name = session['name']
    
    # Get available names
    assignments_df = load_assignments()
    available_names = list(employees_df['Full Name'].values)
    available_names.remove(person_name)
    
    for assigned in assignments_df['Assigned_To'].values:
        if assigned in available_names:
            available_names.remove(assigned)
    
    if not available_names:
        return jsonify({'success': False, 'message': 'No more assignments available'})
    
    # Create random numbers list
    random.shuffle(available_names)
    numbers = list(range(1, len(available_names) + 1))
    random.shuffle(numbers)
    
    # Store in session
    session['available_names'] = available_names
    session['numbers'] = numbers
    
    return jsonify({'success': True, 'numbers': numbers})

@app.route('/flip_card', methods=['POST'])
def flip_card():
    if 'email' not in session or 'available_names' not in session:
        return jsonify({'success': False, 'message': 'Session expired'})
    
    number = request.json.get('number')
    email = session['email']
    person_name = session['name']
    available_names = session['available_names']
    
    # Random assignment
    assigned_name = random.choice(available_names)
    
    # Save to Excel
    save_assignment(email, person_name, assigned_name)
    
    # Clear session
    session.clear()
    
    return jsonify({'success': True, 'name': assigned_name})

if __name__ == '__main__':
    app.run(debug=False)