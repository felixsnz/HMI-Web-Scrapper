import random
from datetime import datetime
from string import ascii_letters, digits
from sql.db_manager import DBManager
import configparser

# Read database configuration
config = configparser.ConfigParser()
config.read('config.ini')

host = config['sql']['host']
database = config['sql']['database']
user = config['sql']['user']
password = config['sql']['password']


# Function to generate random alphanumeric strings
def generate_random_string(length, int_perc=0.9):
    numeric_length = int(length * int_perc)  # Calculate the length for numeric characters
    characters = digits * numeric_length  # Include only digits (numeric characters)
    characters += ascii_letters  # Include remaining characters (letters)
    return ''.join(random.sample(characters, length)).upper()  # Shuffle the characters

# Function to generate random boolean values
def generate_random_boolean():
    return random.choices([True, False], weights=[0.95, 0.05], k=1)[0]

# Function to generate random float values
def generate_random_float():
    random_float = random.uniform(0, 100)
    rounded_float = round(random_float, 4)
    return rounded_float


# Function to generate random float values with lower and upper bounds
def generate_random_float_bounds(lower_bound=0, upper_bound=100):
    random_float = random.uniform(lower_bound, upper_bound)
    rounded_float = round(random_float, 4)
    return rounded_float

# Function to generate a set of minimum, maximum, and measured values
def generate_random_measurement(tolerance=0.1):
    min_val = generate_random_float()
    max_val = min_val + generate_random_float_bounds()  # Ensure max_val is always greater than min_val

    # Determine bounds for the measured value, allowing for some tolerance outside min and max
    lower_bound = min_val - (tolerance * min_val)
    upper_bound = max_val + (tolerance * max_val)
    measured_val = generate_random_float_bounds(lower_bound, upper_bound)

    return min_val, max_val, measured_val
def generate_random_units():

    
    my_list = ['Volts', 'Amps', 'Ohms']
    return random.choice(my_list)



# Create an instance of the DBManager class
db_manager = DBManager(server=host, database=database, user=user, password=password)

# Connect to the database
db_manager.connect()

# Specify the table name
table_name = 'E28'

# Generate random values and insert into the table
for _ in range(10):  # Change the number to the desired amount of rows

    # Generate random values for the first set of measurements
    min_val1, max_val1, measured_val1 = generate_random_measurement()

    # Generate random values for the second set of measurements
    min_val2, max_val2, measured_val2 = generate_random_measurement()

    # Generate random values for the third set of measurements
    min_val3, max_val3, measured_val3 = generate_random_measurement()

    min_val4, max_val4, measured_val4 = generate_random_measurement()

    min_val5, max_val5, measured_val5 = generate_random_measurement()

    min_val6, max_val6, measured_val6 = generate_random_measurement()

    # Continue generating sets of measurements as needed...
    data = [
        datetime.now(),  # Timestamp
        generate_random_string(8, 1),  # E28.EmployeeNumber
        generate_random_string(11),  # E28.SerialNumber
        generate_random_string(6),  # E28.YorkPN
        generate_random_boolean(),  # E28._7_3_ConnectionsOk
        generate_random_boolean(),  # E28._7_3_ContinuityToRed
        generate_random_boolean(),  # E28._7_3_ContinuityToBlack
        generate_random_boolean(),  # E28._7_3_ContinuityToWhite
        generate_random_boolean(),  # E28._7_4_7_5_ConnectionsOk
        generate_random_boolean(),  # E28._5_1_AtoC_HighPotOk
        generate_random_boolean(),  # E28._5_1_D_HighPotOk
        generate_random_boolean(),  # E28._5_1_E_ConnectionsOk
        generate_random_boolean(),  # E28._6_1_JumpersOk
        generate_random_boolean(),  # E28._7_8_SDCardProgrammingOk
        generate_random_boolean(),  # E28._7_9_A_KeypadProcess
        generate_random_boolean(),  # E28._7_9_B_KeypadProcess
        generate_random_boolean(),  # E28._7_9_C_KeypadProcess
        generate_random_boolean(),  # E28._7_9_D_SerialPortTesting
        generate_random_boolean(),  # E28._7_9_E_AutoTesting
        generate_random_boolean(),  # E28._7_9_F_LampsTesting
        measured_val1,    # E28._7_9_G_MeasuredVoltage
        min_val1,    # E28._7_9_G_MinimumValue
        max_val1,    # E28._7_9_G_MaximumValue
        generate_random_units(),  # E28._7_9_G_MeasurementUnit
        generate_random_boolean(),  # E28._7_9_H_DipSwitchChanging
        generate_random_boolean(),  # E28._7_10_KeypadProcess
        generate_random_boolean(),  # E28._7_11_KeypadProcess
        generate_random_boolean(),  # E28._7_12_KeypadProcess
        generate_random_boolean(),  # E28._7_14_KeypadProcess
        generate_random_boolean(),  # E28._7_15_CommsTesting
        measured_val2, # E28._7_16_306302_MeasuredVoltage
        min_val2, # E28._7_16_306302_MinimumValue
        max_val2, # E28._7_16_306302_MaximumValue
        generate_random_units(), # E28._7_16_306302_MeasurementUnit
        measured_val3, # E28._7_16_30608_MeasuredVoltage
        min_val3, # E28._7_16_30608_MinimumValue
        max_val3, # E28._7_16_30608_MaximumValue
        generate_random_units(), # E28._7_16_30608_MeasurementUnit
        measured_val4, # E28._7_16_306310_MeasuredVoltage
        min_val4, # E28._7_16_306310_MinimumValue
        max_val4, # E28._7_16_306310_MaximumValue
        generate_random_units(), # E28._7_16_306310_MeasurementUnit
        measured_val5, # E28._7_16_306313_MeasuredVoltage
        min_val5, # E28._7_16_306313_MinimumValue
        max_val5, # E28._7_16_306313_MaximumValue
        generate_random_units(), # E28._7_16_306313_MeasurementUnit
        generate_random_boolean(), # E28._7_16_ProcessDone
        generate_random_boolean(), # E28._7_17_KeypadProcess
        measured_val6, # E28._7_6_MeasuredVoltage
        min_val6, # E28._7_6_MinimumValue
        max_val6, # E28._7_6_MaximumValue
        generate_random_units(), # E28._7_6_MeasurementUnit
        generate_random_boolean(), # E28._7_6_ProcessDone
        generate_random_boolean() #E28._7_7_PowerSupplyWiringTest
    ]

    db_manager.insert(table_name, data)
db_manager.disconnect()
