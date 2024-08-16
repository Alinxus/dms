from flask import Flask, render_template, request, redirect, url_for, flash
import os
import asyncio
from send import main  # Assuming your existing DM sending code is in send.py

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key

# Ensure the upload folder exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['csv_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Get Instagram credentials and proxy
            username = request.form['username']
            password = request.form['password']
            proxy = request.form.get('proxy')

            # Set environment variables for messages
            os.environ['INSTAGRAM_USERNAME'] = username
            os.environ['INSTAGRAM_PASSWORD'] = password
            if proxy:
                os.environ['PROXY'] = proxy

            # Run the main async function for sending DMs
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main([], [file_path]))  # Assuming main function accepts file path

            flash('Messages sent successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload a CSV file.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
