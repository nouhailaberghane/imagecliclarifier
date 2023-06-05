from flask import Flask, render_template, request, send_from_directory
import subprocess
import os

import datetime


app = Flask(__name__)

# index page--------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

#  upload page------------------------------------------------------------------------

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
# Handle the file upload logic ------------------------------------------------------
        global filename
        filename = file.filename
        file.save('demo/' + filename)
        return render_template('clair.html')
    else:
        return "No file specified."
    
# clair page -----------------------------------------------------------------------
    
@app.route('/executer_script')
def executer_script():
    # Code à exécuter lorsque le bouton est cliqué
    arg = "-ul"
    subprocess.run(['python', 'demo.py', arg ])

    return render_template('download.html')

# download page ---------------------------------------------------------------------

@app.route('/download')
def download():
    folder = 'demo/enhanced'  # Directory where the file is stored
    
    file =  filename # Use the variable corrected_name
    
    if filename:
        return send_from_directory(folder, file, as_attachment=True)
    else:
        return "File not found."
 

# supprimer old image -----------------------------------------------------------------
folder_path1 = 'demo/enhanced'
folder_path2 = 'demo'


def delete_files_after_5min(folder_path):
    file_list = os.listdir(folder_path)  # Get a list of all files in the folder

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)  # Construct the full file path

        # Check if the path points to a file
        if os.path.isfile(file_path):
            # Get the modification time of the file
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            # Calculate the time elapsed since the file modification
            time_elapsed = datetime.datetime.now() - modification_time

            # Check if the time elapsed is greater than or equal to 24 hours
            if time_elapsed >= datetime.timedelta(minutes=5):
                # Delete the file
                os.remove(file_path)



delete_files_after_5min(folder_path1)
delete_files_after_5min(folder_path2)


if __name__ == '__main__':
    app.run()
