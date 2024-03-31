import warnings
warnings.filterwarnings('ignore')
import os
import plotly.graph_objects as go

from flask import Flask, render_template, redirect, url_for, request

from processing.pre_process_data import (extract_most_recent_data,
                                         FILE_PATH_PATTERN)

from processing.plotly_visuals import (total_economic_activty_overtime,
                                       breakdown_reason_of_economic_inactivity)


app = Flask(__name__)


@app.route('/')
def index():
    date_pattern = extract_most_recent_data().\
            split('src/data/inac01sa')[1].split('.xls')[0].capitalize()

    return render_template('index.html', recent_date=date_pattern)


@app.route('/route_trend_analysis')
def route_trend_analysis():
    return redirect(url_for('trend_analysis'))

@app.route('/trend_analysis')
def trend_analysis():
    return render_template('trend_analysis.html',
                           plot=total_economic_activty_overtime().to_html(full_html=False), 
                           plot2=breakdown_reason_of_economic_inactivity().to_html(full_html=False))



@app.route('/redirect_gender_analysis')
def route_gender_breakdown():
    return redirect(url_for('gender_breakdown_analysis'))

@app.route('/gender_analysis')
def gender_breakdown_analysis():

    return render_template('gender_breakdown.html',
                           plot=total_economic_activty_overtime().to_html(full_html=False), 
                           plot2=total_economic_activty_overtime().to_html(full_html=False))









#########################
# Future CODE - for updating the dashboard with newer data
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
