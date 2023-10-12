# CS50 Python Final Project - A program calculating the parameters of a mortgage loan.

This is the program that calculates various parameters of a mortgage loan. 
It was prepared as a final project of the course - **"CS50’s Introduction to Programming with Python".**  

#### Course page: 
https://cs50.harvard.edu/python/2022/

#### Final project requirements:
https://cs50.harvard.edu/python/2022/project/

_Thank you to everyone involved in creating this very valuable course!_ 

#### Video Demo
https://youtu.be/jt-Iw8lga-w

## Available functionalities
### Main:
- calculate the total amount to be repaid,
- calculate the total interest on the loan,
- calculate monthly payment:
  - constant for equal installments,
  - first month payment for decreasing installments,
- generate basic payment schedule, including for each month:
  - installment amount,
  - amount remaining to be repaid
### Optional - calculations related to overpayment:
- calculate lower monthly payment after one-time overpayment,
- generate new payment schedule considering overpayment,
- calculate total savings resulting from overpayment,

### Additional calculations related to the mortgage:
- calculate savings resulting from the choice of decreasing installments.

## Input
### Required:
- Loan amount, USD.
- Nominal interest rate, %.
- Repayment period, months.
- Type of installments (equal or decreasing).

### Optional:
- Amount of overpayment, USD.

## Output
### Data frames:
- **mortgage attributes sheet:**
  - Loan amount,
  - Nominal interest rate,
  - Repayment period,
  - Type of installments,
  - Overpayment (if given)
- **calculation summary:**
  - Total amount remaining to be repaid,
  - Total interest,
  - Monthly payment,
  - (if overpayment is given):
    - Overpayment saving,
    - New total amount remaining to be repaid,
    - New total interest,
    - New monthly payment.
- **payment schedule:**
  - installment amount for each month
  - new installment amount for each month (if overpayment is given),
  - amount remaining to be paid for each month
  - new amount remaining to be paid for each month (if overpayment is given),

### Functions available for external calculation:

- **generate_mortgage_attributes_sheet** - Using the Mortgage class, the function generates a mortgage attributes sheet.

- **calculate_overpayment_saving** - Using the Mortgage class, the function calculates total savings resulting from the overpayment.

- **calculate_decreasing_installments_saving** - Using the Mortgage class, the function calculates savings resulting from the choice of decreasing installments.

## How to run "project.py" file - example usage of Mortgage class
The Mortgage class can be called from and used in other programs. 
A sample use of its capabilities as well as results presentation has been prepared 
in the main function. It can be used from the command line terminal after navigating 
to the folder where the program is saved and executing it with input parameters.

### Step by step:

1. Open terminal.
2. Navigate to the folder where the program is located.
3. Run the program with all input parameters as described in below.

### Input parameters:


    --loan -l Loan amount, USD, type=int
    --rate -r Nominal interest rate (per year), %, type=int
    --months -m Repayment period, months, type=int
    --installments -i Type of installments, "equal" or "decreasing", type=str
    --overpayment -o (optional) Overpayment value, USD, type=float


### Examples:

    python project.py -loan=50000 -rate=7 -months=60 -installments='equal'
    
    python project.py -l=50000 -r=7 -m=60 -i='equal' -overpayment=5000 
    
    python project.py -l=50000 -r=7 -m=60 -i='decreasing'
    
    python project.py -l=50000 -r=7 -m=60 -i='decreasing' -o=5000



## How to use Mortgage class
The Mortgage class can be called from and used in other programs. 

1. Import Mortgage class.
2. Create an instance of the class entering all required input values (the last parameter (overpayment) may or may not be given)
3. Initialization of the object will run all calculations and their results will be stored as object attributes.
4. Then you can call the created object to use the described functionalities (see examples below).

### Example:

Initialization of the object

    mortgage = Mortgage(50000, 7, 60, 'equal', 5000)

    mortgage = Mortgage(10000, 5, 60, 'decreasing')

Calling results:

    mortgage.mortgage_attributes_sheet

Printing results:

    print(mortgage.mortgage_attributes_sheet)

Saving generated payment schedule(s) to .csv file using save_schedule_to_csv method:

    mortgage.save_schedule_to_csv("Payment_schedule.csv")

## How to use external functions
External functions using mortgage class can be called from other program as well:

    project.generate_mortgage_attributes_sheet(50000, 7, 60, 'equal', 5000)

    project.calculate_overpayment_saving(50000, 7, 60, 'equal', 5000)

    project.calculate_decreasing_installments_saving(50000, 7, 60)

## How to execute pytest testing

1. Open terminal.
2. Navigate to the folder where the program is located.
3. Run below command to run all tests:


    pytest test_project.py

4. Or run only group of tests:
 

    pytest test_project.py -m <markername>

Available markernames:

- main_functionalities_testing
- external_functions_testing
- exception_handling_testing_external_functions
- exception_handling_testing_object_init
- exception_handling_testing_wrong_format
- exception_handling_testing_logically_incorrect_input
