from flask import Flask, render_template, request
from converters import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    result = None
    category = 'length'
    from_unit = to_unit = value = ''

    categories = {
        'length': ['millimeter', 'centimeter', 'meter', 'kilometer', 'inch', 'foot', 'yard', 'mile'],
        'weight': ['milligram', 'gram', 'kilogram', 'ounce', 'pound'],
        'temperature': ['Celsius', 'Fahrenheit', 'Kelvin']
    }

    if request.method == 'POST':
        category = request.form.get('category')
        from_unit = request.form.get('from_unit')
        to_unit = request.form.get('to_unit')
        value = request.form.get('value')

        if category and from_unit and to_unit and value:
            if category == 'length':
                result = length(from_unit, to_unit, value)
            elif category == 'weight':
                result = weight(from_unit, to_unit, value)
            elif category == 'temperature':
                result = temperature(from_unit, to_unit, value)

    return render_template('converter.html',
                           result=result,
                           category=category,
                           categories = categories.keys(),
                           units = categories[category],
                           from_unit = from_unit,
                           to_unit = to_unit,
                           value = value
                           )


if __name__ == '__main__':
    app.run(debug=True)