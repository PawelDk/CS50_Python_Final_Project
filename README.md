# CS50_Python_Final_Project

This is the program that calculates various parameters of a mortgage loan.

#Planned functionalities:
####Main:
- calculate the total amount to be paid,
- calculate the total interest on the loan,
- calculate monthly payment (first month payment for decreasing installments),
- generate basic payment schedule, including for each month:
  - installment amount
  - remaining amount
####Optional:
- calculate effect of one-time overpayment (lower monthly payment)
- generate payment schedule with overpayment
- calculate total savings resulting from overpayment

#Input:
####Main:
- Loan amount, USD.
- Nominal interest rate, %.
- Repayment period, months.
- Type of installments [equal, decreasing].

####Optional:
- Amount of overpayment, USD.

#Output:
### Data frames:
- mortgage sheet
- calculation summary
- payment schedule (with or without overpayment)

Functions available for external calculation:
- generate_mortgage_sheet
- calculate_overpayment_saving
- calculate_decreasing_installments_saving