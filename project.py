import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--loan', '-l', help="Loan amount, USD", type=int)
parser.add_argument('--rate', '-r', help="Nominal interest rate (per year), %", type=int)
parser.add_argument('--months', '-m', help="Repayment period, months", type=int)
parser.add_argument('--inst', '-i', help="Type of installments [equal, decreasing]", type=str)

class Mortgage:
    def __init__(self, loan_amount, nominal_rate, period_in_months, installments_type):
        self.loan_amount = loan_amount
        self.nominal_rate = nominal_rate
        self.period_in_months = period_in_months
        self.installments_type = installments_type
        self.monthly_payment = self.calculate_monthly_payment()

    @property
    def loan_amount(self):
        return self._loan_amount

    @loan_amount.setter
    def loan_amount(self, loan_amount):
        if loan_amount <= 0:
            raise ValueError
        self._loan_amount = loan_amount

    @property
    def nominal_rate(self):
        return self._nominal_rate

    @nominal_rate.setter
    def nominal_rate(self, nominal_rate):
        if nominal_rate <= 0:
            raise ValueError
        self._nominal_rate = nominal_rate

    @property
    def period_in_months(self):
        return self._period_in_months

    @period_in_months.setter
    def period_in_months(self, period_in_months):
        if period_in_months <= 0:
            raise ValueError
        self._period_in_months = period_in_months

    @property
    def installments_type(self):
        return self._installments_type

    @installments_type.setter
    def installments_type(self, installments_type):
        if installments_type not in ['equal', 'decreasing']:
            raise ValueError
        self._installments_type = installments_type

    def calculate_monthly_payment(self):
        if self.installments_type == 'equal':
            sigma = 0
            i = 1
            while i <= self.period_in_months:
                sigma += (1 + self.nominal_rate / 100 / 12) ** (-i)
                i += 1
            monthly_payment = self.loan_amount / sigma
            return monthly_payment

        elif self.installments_type == 'decreasing':
            first_month_payment = self.loan_amount / self.period_in_months * (1 + (self.period_in_months * self.nominal_rate / 100 / 12))
            return first_month_payment

    # def calculate_total_amount(self, loan, r, m,):
    #     if self.installments_type == 'equal':
    #         return m * self.monthly_payment_equal(loan, r, m)
    #     elif self.installments_type == 'decreasing':
    #         schedule = self.monthly_payment_decreasing(args.loan, args.rate, args.months)
    #         return sum(schedule)
    #     else:
    #         print("inst value not known")
    #         return


# def monthly_payment_decreasing(loan, r, m):
#     schedule = []
#     for n in reversed(range(1, m+1)):
#         installment = loan/m * (1 + (n * r/100/12))
#         schedule.append(installment)
#
#     return schedule


if __name__ == '__main__':
    args = parser.parse_args()
    mortgage = Mortgage(args.loan, args.rate, args.months, args.inst)

    # total_amount_result = total_amount(args.loan, args.rate, args.months, args.inst)
    # print("Total amount: " + str(total_amount_result))
    # print("Total interest: " + str(total_amount_result - args.loan))
    #
    # if args.inst == 'equal':
    #     print("Installment: " + str(monthly_payment_equal(args.loan, args.rate, args.months)))
    # elif args.inst == 'decreasing':
    #     print("First installment: " + str(monthly_payment_decreasing(args.loan, args.rate, args.months)[0]))
    # else:
    #     print("inst value not known")




