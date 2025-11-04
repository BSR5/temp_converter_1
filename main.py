fixed_conversion_rates = {
    "distance": {"miles_to_kilometers": 1.60934, "kilometers_to_miles": 0.621371},
    "weight": {"pounds_to_kilograms": 0.453592, "kilograms_to_pounds": 2.20462}
}

def inputs():
    user_input = input("Please enter the conversion (e.g. 25 miles to kilometers): ")
    words = user_input.split()
    found = False
    for i, word in enumerate(words):
        if word.lower() == "to":
            from_unit = words[i - 1]
            to_unit = words[i + 1]
            value = float(words[i - 2])
            found = True
    if found == False or len(words) < 4:
        raise Exception("Invalid input")
    return from_unit.lower(), to_unit.lower(), value

def temp_f_to_c(fahrenheit):
    celcius = (fahrenheit - 32) * (5 / 9)
    return celcius

def temp_c_to_f(celsius):
    fahrenheit = (celsius * (9 / 5) + 32)
    return fahrenheit

def convert_fixed(unit_type, from_unit, to_unit, from_unit_value):
    rate_key = f"{from_unit}_to_{to_unit}"
    rate = fixed_conversion_rates[unit_type][rate_key]
    return from_unit_value * rate

def convert_temp(from_unit, from_unit_value):
    if from_unit.lower() == "celsius":
        value = temp_c_to_f(from_unit_value)
        to_unit = "Fahrenheit"
    elif from_unit.lower() == "fahrenheit":
        value = temp_f_to_c(from_unit_value)
        to_unit = "Celsius" 
    return value, to_unit

def type_check(from_unit, to_unit):
    rate_key = f"{from_unit}_to_{to_unit}"
    found = False
    for type in fixed_conversion_rates:
        if rate_key in fixed_conversion_rates[type]:
            unit_type = type
            found = True
    if found == False:
        unit_type = "temperature"
    return unit_type

def convert(unit_type, from_unit, to_unit, value):
    if unit_type in fixed_conversion_rates:
        final_value = convert_fixed(unit_type, from_unit, to_unit, value)
    elif unit_type == "temperature":
        final_value = convert_temp(from_unit, value)
    else:
        raise Exception("This conversion has not yet been added")
    return final_value

def main():
    while True:
        try:
            from_unit, to_unit, value = inputs()
            unit_type = type_check(from_unit, to_unit)
            result = convert(unit_type, from_unit, to_unit, value)
            if isinstance(result, tuple):
                value_converted, to_unit = result
            else:
                value_converted = result
            print(f"{value} {from_unit} is {value_converted:.2f} {to_unit}")
        except Exception as e:
            print(f"Error: {e}")
        again = input("Do you want to convert another value? (yes/no): ").strip().lower()
        if again != "yes":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
