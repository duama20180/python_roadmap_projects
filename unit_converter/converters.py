# Length: millimeter, centimeter, meter, kilometer, inch, foot, yard, mile.
# Weight: milligram, gram, kilogram, ounce, pound.
# Temperature: Celsius, Fahrenheit, Kelvin.

def length(input_type, output_type, input_value):
    lengths = {
        "millimeter": (0.001, "mm"),
        "centimeter": (0.01,"cm"),
        "meter": (1,"m"),
        "kilometer": (1000, "km"),
        "inch": (0.0254,"in"),
        "foot": (0.3048, "ft"),
        "yard": (0.9144,"yd"),
        "mile": (1609.344, "mi")
    }
    try:
        output_value =  int(input_value) * lengths[input_type][0] / lengths[output_type][0]
        return f"{input_value} {lengths[input_type][1]} = {output_value:.10} {lengths[output_type][1]}"
    except ValueError:
        return None

def weight(input_type, output_type, input_value):
    weights = {
        'milligram' : (0.001, "mg"),
        'gram' : (1, "g"),
        'kilogram' : (1000, "kg"),
        'ounce' : (28.3495231, "oz"),
        'pound' : (453.59237, "lb")
    }
    try:
        output_value =  int(input_value) * weights[input_type][0] / weights[output_type][0]
        return f"{input_value} {weights[input_type][1]} = {output_value:.10} {weights[output_type][1]}"
    except ValueError:
        return None

def temperature(input_type, output_type, input_value):
    try:
        value = float(input_value)

        if input_type == 'Fahrenheit':
            value = (value - 32) * 5 / 9
        elif input_type == 'Kelvin':
            value = value - 273.15

        if output_type == 'Fahrenheit':
            result = (value * 9 / 5) + 32
        elif output_type == 'Kelvin':
            result = value + 273.15
        else:
            result = value

        symbols = {
            'Celsius': '℃',
            'Fahrenheit': '℉',
            'Kelvin': 'K'
        }

        return f"{input_value} {symbols[input_type]} = {result:.2f} {symbols[output_type]}"
    except:
        return None


def main():
    test = length("millimeter", "kilometer", 1)
    print(test)
    test = weight("gram", "kilogram", 1)
    print(test)
    test = weight("kilogram", "pound", 1)
    print(test)
    test = temperature("Celsius", "Fahrenheit", 1)
    print(test)

if __name__ == "__main__":
    main()