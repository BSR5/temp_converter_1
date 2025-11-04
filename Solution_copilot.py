from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

# --- Conversion Data ---
fixed_conversion_rates = {
    "distance": {"miles_to_kilometers": 1.60934, "kilometers_to_miles": 0.621371},
    "weight": {"pounds_to_kilograms": 0.453592, "kilograms_to_pounds": 2.20462}
}

# --- Result Structure ---
@dataclass
class ConversionResult:
    value: float
    to_unit: str

# --- Abstract Base Converter ---
class BaseConverter(ABC):
    @abstractmethod
    def __call__(self, from_unit: str, to_unit: str, value: float) -> ConversionResult:
        pass

# --- Fixed Rate Converter ---
class FixedRateConverter(BaseConverter):
    def __init__(self, unit_type: str):
        self.unit_type = unit_type
        self.rates = fixed_conversion_rates[unit_type]

    def __call__(self, from_unit, to_unit, value):
        rate_key = f"{from_unit}_to_{to_unit}"
        rate = self.rates.get(rate_key)
        if rate is None:
            raise ValueError(f"No conversion rate for {from_unit} to {to_unit}")
        return ConversionResult(value=value * rate, to_unit=to_unit)

# --- Temperature Converter ---
class TemperatureConverter(BaseConverter):
    def __call__(self, from_unit, to_unit, value):
        match (from_unit.lower(), to_unit.lower()):
            case ("celsius", "fahrenheit"):
                result = value * 9 / 5 + 32
            case ("fahrenheit", "celsius"):
                result = (value - 32) * 5 / 9
            case _:
                raise ValueError("Unsupported temperature conversion.")
        return ConversionResult(value=result, to_unit=to_unit)

# --- Converter Factory ---
class ConverterFactory:
    @staticmethod
    def get_converter(from_unit: str, to_unit: str) -> BaseConverter:
        rate_key = f"{from_unit}_to_{to_unit}"
        for unit_type, conversions in fixed_conversion_rates.items():
            if rate_key in conversions:
                return FixedRateConverter(unit_type)
        return TemperatureConverter()

# --- Input Parser ---
def parse_input() -> tuple[str, str, float]:
    user_input = input("Enter conversion (e.g. 25 miles to kilometers): ").strip().lower()
    words = user_input.split()

    if "to" not in words or len(words) < 4:
        raise ValueError("Invalid input format. Use: '<value> <from_unit> to <to_unit>'")

    try:
        to_index = words.index("to")
        value = float(words[to_index - 2])
        from_unit = words[to_index - 1]
        to_unit = words[to_index + 1]
    except (IndexError, ValueError):
        raise ValueError("Invalid input. Ensure format and numeric value are correct.")

    return from_unit, to_unit, value

# --- Main Loop ---
def main():
    while True:
        try:
            from_unit, to_unit, value = parse_input()
            converter = ConverterFactory.get_converter(from_unit, to_unit)
            result = converter(from_unit, to_unit, value)
            print(f"{value} {from_unit} is {result.value:.2f} {result.to_unit}")
        except Exception as e:
            print(f"Error: {e}")

        if input("Convert another? (yes/no): ").strip().lower() != "yes":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()