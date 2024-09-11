# app.py

from flask import Flask, render_template
from report_generator.xml_parser import parse_all_xml

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Parse all XML files from the 'data/' directory and aggregate the results
    report_data = parse_all_xml('data/')
    #print(report_data)
    return render_template('index.html', report_data=report_data)

if __name__ == '__main__':
    app.run(debug=True)
