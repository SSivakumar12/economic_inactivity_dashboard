import warnings
warnings.filterwarnings('ignore')
import os
import re
import plotly.io
import pandas as pd

from flask import Flask, render_template, redirect, url_for, request, jsonify


from processing.pre_process_data import extract_most_recent_data, FILE_PATH_PATTERN

from processing.plotly_visuals import (total_economic_activty_overtime,
                                       breakdown_reason_of_economic_inactivity,
                                       economic_inactivity_wanting_a_job,
                                       breakdown_of_economic_inactivity_by_gender,
                                    #    WOMEN_DATA, MEN_DATA
                                       )


app = Flask(__name__)
BASE_TITLE = "Breakdown of reasons for economic inactivity overtime"


@app.route('/')
def index():
    date_pattern =\
        pd.read_excel(extract_most_recent_data(), 'People').iloc[0, 1].strftime("%B%Y")
    return render_template('index.html', recent_date=date_pattern)


@app.route('/route_trend_analysis')
def route_trend_analysis():
    return redirect(url_for('trend_analysis'))

@app.route('/trend_analysis')
def trend_analysis():
    return render_template(
        'trend_analysis.html',
        plot=total_economic_activty_overtime().to_html(full_html=False), 
        plot2=breakdown_reason_of_economic_inactivity(title=BASE_TITLE,
                                                      column="Long-term sick").to_html(full_html=False),
        plot3=economic_inactivity_wanting_a_job().to_html(full_html=False)
        )



@app.route('/redirect_gender_analysis')
def route_gender_breakdown():
    return redirect(url_for('gender_breakdown_analysis'))

@app.route('/gender_analysis')
def gender_breakdown_analysis():
    men_title = f'{BASE_TITLE} in men'
    women_title = f'{BASE_TITLE} in women'
    return render_template('gender_breakdown.html')

    # return render_template(
    #     'gender_breakdown.html',
    #     plot=breakdown_of_economic_inactivity_by_gender().to_html(full_html=False), 
    #     plot2=breakdown_reason_of_economic_inactivity(title=men_title,
    #                                                   column="Long-term sick",
    #                                                   data=MEN_DATA).to_html(full_html=False),
    #     plot3=breakdown_reason_of_economic_inactivity(title=women_title,
    #                                                   column="Looking after family / home",
    #                                                   data=WOMEN_DATA).to_html(full_html=False)
    #     )                                              
plot1_data = total_economic_activty_overtime().to_html(full_html=True)
plot2_data = total_economic_activty_overtime().to_html(full_html=True)                                                   

@app.route('/update_visuals', methods=['GET'])
def update_visuals():
    value = int(request.args.get('value', 1993))  # Get slider value from request
    # Update Plotly visuals based on the slider value
    updated_plot1_html = update_plot_html(plot1_data, value)
    updated_plot2_html = update_plot_html(plot2_data, value)
    return jsonify({'plot1': updated_plot1_html, 'plot2': updated_plot1_html})


def update_plot_html(plot_html, value):
    # Modify the HTML content of the Plotly visual based on the slider value
    # Implement your logic to update the HTML content here
    # For demonstration, let's replace a placeholder value in the HTML content
    updated_html = plot_html.replace('placeholder_value', str(value))
    return updated_html







#########################
# Future CODE - for updating the dashboard with newer data
# considerations 
#   - how to ensure we validate right data being stored
#   - how do we ensure only certain people can update the dashboard
######################

@app.route('/test_form')
def upload_file():
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
  return render_template('form.html')


if __name__ == '__main__':
    # REMEMBER IF YOU AND SENDING TO PRODUCTION COMMENT OUT LINE 102
    # IF YOU ARE IN DEV COMMENT OUT 99/100
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


    # app.run(debug=True)
