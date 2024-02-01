from flask import Flask, render_template, request,redirect, url_for,jsonify
from send_email_function import send_email_function
from random_otp import random_otp
from flask_cors import CORS  # Import the CORS module
from check_wifi import get_signal_strength
from face_recognizer import detect_and_match_face
from google_sheets_function import google_sheets_function
from email_rollnumber_mapping import email_rollnumber_mapping
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
credentials = {}

emails={
    'Yash_Padale':'yashpadale108@gmail.com',
    #'Yash_Talegaonkar':'yashpadale108@gmail.com',
    'krishna_pardeshi':'krishrp22@gmail.com',
    #'Roshan_bansode':'yashpadale108@gmail.com'
        }

image_ = {
    'images/krishna_pardeshi.jpg': 'krishna_pardeshi',
    'images/Roshan_bansode.jpeg': 'Roshan_bansode',
    'images/Yash.jpeg': 'Yash_Padale',
    'images/YashT.jpeg': 'Yash_Talegaonkar'
}

#image_locations = ['C:/Users/yashp/PycharmProjects/Face_Recognition_Flask/images/Yash.jpeg', 'C:/Users/yashp/PycharmProjects/Face_Recognition_Flask/images/YashT.jpeg']
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    name = request.form.get('name')
    otp = random_otp()
    send_email_function(subject="Making Attendance Easy", body=f"Dear {name}, Your OTP is {otp}", to_email=name)
    credentials[name] = otp
    return render_template('enter_otp_page.html', email=name)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    digit1 = request.form.get('digit1')
    digit2 = request.form.get('digit2')
    digit3 = request.form.get('digit3')
    digit4 = request.form.get('digit4')
    entered_otp = digit1 + digit2 + digit3 + digit4
    stored_otp = credentials.get(email)
    print(f'The entered otp is - {entered_otp} The stored_otp is {stored_otp} ')
    if int(entered_otp) == stored_otp:
        return render_template('Latitude_longitude_page.html', email=email)
    else:
        return f'The OTP for {email} is incorrect.'

@app.route('/attendance_marked', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        email = request.form.get('email')
        print(f'The email received from the form is: {email}')
        return render_template('wifi_strength.html',email=email)

@app.route('/check_wifi_strength', methods=['POST'])
def wifi_strength_check():
    if request.method == 'POST':
        email = request.form.get('email')
        print(f'The email received from the form is: {email}')

        ssid_to_check = "Krishna"
        signal_strength = get_signal_strength(ssid_to_check)
        print(f'detected signal_strength is {signal_strength}')

        if signal_strength <= 50:
            return render_template('face_recognition.html', email=email)
        else:
            return f"You are not in the classroom. Email: {email}"
    else:
        # Handle the case where the route is accessed using GET method
        return "Invalid request method"

def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key

@app.route('/upload', methods=['POST'])
def upload():
    print('Receiving video data...')
    video = request.files['video']
    email = request.form.get('email')
    original_video_path = os.path.join(os.getcwd(), 'uploaded_video.webm')
    video.save(original_video_path)
    image_keys = list(image_.keys())
    image_values = list(image_.values())
    index = detect_and_match_face(video_path=original_video_path, image_locations=image_keys)
    detected_person_name = image_values[index]
    email_of_detected_person = emails.get(detected_person_name)
    print(f'The person detected is - {detected_person_name}')
    person=find_key_by_value(dictionary=emails,target_value=email)
    print(f'The person entered is  {person}')
    print(f'The email of detected person is - {email_of_detected_person}')
    print(f'The email received is - {email}')
    os.remove(original_video_path)
    if email_of_detected_person == email:
        print('Hare krishna congrats')
        return jsonify({'success': True, 'redirect_url': url_for('congrats', email=email, detected_person=detected_person_name, entered_person=person)})
    else:
        print('Person not detected correctly')
        return jsonify({'success': False, 'message': 'Person not detected correctly'})

@app.route('/congrats')
def congrats():
    detected_person = request.args.get('detected_person')
    # google_sheets_function(name=detected_person)
    entered_person = request.args.get('entered_person')
    email = request.args.get('email')
    roll_number = email_rollnumber_mapping.get(email)
    google_sheets_function(email, roll_number)
    return render_template('simple.html', email=email, detected_person=detected_person, entered_person=entered_person)

@app.route('/failure_url')
def failure_url():
    return render_template('failure.html')


if __name__ == '__main__':
    app.run( debug=True)
    #app.run(host='0.0.0.0', port=5000,debug=True)
