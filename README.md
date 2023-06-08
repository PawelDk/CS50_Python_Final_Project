# CS50_Python_Final_Project

This is the program that calculates various parameters of a mortgage loan.

#Available functionalities:
####Main:
- calculate the total amount to be repaid,
- calculate the total interest on the loan,
- calculate monthly payment:
  - constant for equal installments,
  - first month payment for decreasing installments,
- generate basic payment schedule, including for each month:
  - installment amount,
  - amount remaining to be repaid
####Optional - calculations related to overpayment:
- calculate lower monthly payment after one-time overpayment,
- generate new payment schedule considering overpayment,
- calculate total savings resulting from overpayment,

####Additional calculations related to the mortgage:
- calculate savings resulting from the choice of decreasing installments.

#Input:
####Main:
- Loan amount, USD.
- Nominal interest rate, %.
- Repayment period, months.
- Type of installments (equal or decreasing).

####Optional:
- Amount of overpayment, USD.

#Output:
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
  - Overpayment saving (if overpayment is given),
  - New total amount remaining to be repaid (if overpayment is given),
  - New total interest (if overpayment is given),
  - New monthly payment (if overpayment is given).
- **payment schedule:**
  - installment amount for each month
  - new installment amount for each month (if overpayment is given),
  - amount remaining to be paid for each month
  - new amount remaining to be paid for each month (if overpayment is given),

### Functions available for external calculation:

- **generate_mortgage_attributes_sheet**

Using the Mortgage class, the function generates a mortgage attributes sheet.

- **calculate_overpayment_saving**

Using the Mortgage class, the function calculates total savings resulting from the overpayment.

- **calculate_decreasing_installments_saving**

Using the Mortgage class, the function calculates savings resulting from the choice of decreasing installments.
