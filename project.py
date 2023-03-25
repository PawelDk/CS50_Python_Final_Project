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
        self.payment_schedule = self.calculate_payment_schedule()
        self.total_amount = self.calculate_total_amount()
        self.total_interest = self.calculate_total_interest()

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

    def calculate_payment_schedule(self):
        keys = range(1, self.period_in_months+1)
        if self.installments_type == 'equal':
            payments = [self.monthly_payment] * self.period_in_months

        elif self.installments_type == 'decreasing':
            payments = []
            for month in reversed(range(1, self.period_in_months + 1)):
                installment = self.loan_amount/self.period_in_months * (1 + (month * self.nominal_rate/100/12))
                payments.append(installment)

        return dict(zip(keys, payments))

    def calculate_total_amount(self):
        total = 0
        for key in self.payment_schedule.keys():
            total += self.payment_schedule[key]
        return total

    def calculate_total_interest(self):
        return self.total_amount - self.loan_amount


if __name__ == '__main__':
    args = parser.parse_args()
    mortgage = Mortgage(args.loan, args.rate, args.months, args.inst)

    print("Total amount: " + str(mortgage.total_amount))
    print("Total interest: " + str(mortgage.total_interest))
    print("Monthly payment: " + str(mortgage.monthly_payment))
    print("Payment schedule:\n" + str(mortgage.payment_schedule))
