def convert_c_to_f(temp_celsius):
    """Transform Celsius into Farenheit"""
    return (temp_celsius * 9/5) + 32

def convert_c_to_k(temp_celsius): 
    """Transform Celsius into Kelvin"""
    return temp_celsius + 273.15

def convert_f_to_c(temp_farenheit):
    """Transform Farenheit into Celsius"""
    return (temp_farenheit - 32) * 5/9

def convert_f_to_k(temp_farenheit):
    """Transform Farenheit into Kelvin"""
    temp_in_celsius = convert_f_to_c(temp_farenheit)
    return convert_c_to_k(temp_in_celsius)

def convert_k_to_c(temp_kelvin):
    """Transform Kelvin into Celsius"""
    return temp_kelvin - 273.15

def convert_k_to_f(temp_kelvin):
    """Transform Kelvin into Farenheit"""
    temp_in_celsius = convert_k_to_c(temp_kelvin)
    return convert_c_to_f(temp_in_celsius)

def show_conversion_options(): 
    """Show availalbe temperature conversions"""
    print("\n" + "-"*55)
    print(" TEMPARATURE CONVERSION TOOL ".center(55))
    print("-"*55)
    print(" [1] Celsius --> Fahrenheit")
    print(" [2] Celsius --> Kelvin")
    print(" [3] Fahrenheit --> Celsius")
    print(" [4] Fahrenheit --> Kelvin")
    print(" [5] Kelvin --> Celsius")
    print(" [6] Kelvin --> Fahrenheit")
    print(" [7] Exit")
    print("-"*55)


def run_converter(): 
    """Execute the temperature conversion program"""
    program_running = True 

    while program_running: 
        show_conversion_options()

        try: 
            user_selection = input("\nSelect an option (1-7): ")

            if user_selection == '7': 
                print({"\nExiting the temperature converter. Goodbye!"})
                program_running = False
                continue

            if user_selection not in ['1', '2', '3', '4', '5', '6']:
                print("\nInvalid selection. Please choose a valid option (1-7).")
                continue

            temperature_value = float(input("Input temperature value:"))

            if user_selection == '1': 
                converted_temp = convert_c_to_f(temperature_value)
                print(f"{temperature_value}°C is {converted_temp:.2f}°F")
            elif user_selection == '2':
                converted_temp = convert_c_to_k(temperature_value)
                print(f"{temperature_value}°C is {converted_temp:.2f}K")
            elif user_selection == '3':
                converted_temp = convert_f_to_c(temperature_value)
                print(f"{temperature_value}°F is {converted_temp:.2f}°C")
            elif user_selection == '4':
                converted_temp = convert_f_to_k(temperature_value)
                print(f"{temperature_value}°F is {converted_temp:.2f}K")
            elif user_selection == '5':
                converted_temp = convert_k_to_c(temperature_value)
                print(f"{temperature_value}K is {converted_temp:.2f}°C")
            elif user_selection == '6':
                converted_temp = convert_k_to_f(temperature_value)
                print(f"{temperature_value}K is {converted_temp:.2f}°F")

        except ValueError: 
            print("\n Error: Please enter a valid numeric value.")
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user. Goodbye!")
            program_running = False 

if __name__ == "__main__": 
    run_converter()
