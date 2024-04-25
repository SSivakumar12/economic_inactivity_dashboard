import warnings
warnings.filterwarnings('ignore')
import os
import re
import pandas as pd

from flask import Flask, render_template, redirect, url_for, request


from processing.pre_process_data import extract_most_recent_data, FILE_PATH_PATTERN

from processing.summary_visuals import visualise_summary_stats
from processing.gender_breakdown_visuals import visualise_gender_breakdown


app = Flask(__name__)

date_pattern =\
    pd.read_excel(extract_most_recent_data(), 'People').iloc[0, 1].strftime("%B%Y")

@app.route('/')
def index():

    return render_template('index.html', recent_date=date_pattern)


@app.route('/route_trend_analysis')
def route_trend_analysis():
    return redirect(url_for('trend_analysis'))

@app.route('/trend_analysis')
def trend_analysis():
    return render_template(
        'trend_analysis.html',
        plot=visualise_summary_stats().to_html(full_html=False),
        date_pattern="Tuesday, 16 April, 2024")

@app.route('/redirect_gender_analysis')
def route_gender_breakdown():
    return redirect(url_for('gender_breakdown_analysis'))

@app.route('/gender_analysis')
def gender_breakdown_analysis():
    return render_template(
        'gender_breakdown.html',
        plot=visualise_gender_breakdown().to_html(full_html=False))                                              
                                                      


#########################
# Future CODE - for updating the dashboard with newer data
# considerations 
#   - how to ensure we validate right data being stored
#   - how do we ensure only certain people can update the dashboard
######################

# @app.route('/test_form', methods=['GET', 'POST'])
# def upload_file():
#   UPLOAD_FOLDER = 'src/data'
#   if request.method == 'POST':
#     uploaded_file = request.files['upload_file']
#     if re.match(FILE_PATH_PATTERN, uploaded_file.filename):
#       filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
#       uploaded_file.save(filepath)
#       print(f"File uploaded successfully. Reload the page.")
#       return redirect(url_for('index'))
#     else:
#       return "No file in the expected format"
#   return render_template('form.html')


if __name__ == '__main__':
    # REMEMBER IF YOU AND SENDING TO PRODUCTION COMMENT OUT LINE 102
    # IF YOU ARE IN DEV COMMENT OUT 99/100
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # app.run(debug=True)
