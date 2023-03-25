import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--loan', '-l', help="Loan amount, USD", type=int)
parser.add_argument('--rate', '-r', help="Nominal interest rate (per year), %", type=int)
parser.add_argument('--months', '-m', help="Repayment period, months", type=int)
parser.add_argument('--installments', '-i', help="Type of installments [equal, decreasing]", type=str)
parser.add_argument('--overpayment', '-o', help="Overpayment value, USD", type=float)
parser.add_argument('--overpayment_type', '-ot', help="Overpayment type [one-time, monthly]", type=str)

class Mortgage:
    def __init__(self, loan_amount, nominal_rate, period_in_months, installments_type, overpayment, overpayment_type):
        self.loan_amount = loan_amount
        self.nominal_rate = nominal_rate
        self.period_in_months = period_in_months
        self.installments_type = installments_type
        self.overpayment = overpayment
        self.overpayment_type = overpayment_type
        self.monthly_payment = self.calculate_monthly_payment()
        self.all_installments = self.calculate_all_installments()
        self.total_amount = self.calculate_total_amount()
        self.total_interest = self.calculate_total_interest()
        self.remaining = self.calculate_remaining()
        self.payment_schedule = self.generate_payment_schedule()

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

    @property
    def overpayment(self):
        return self._overpayment

    @overpayment.setter
    def overpayment(self, overpayment):
        if overpayment <= 0 or overpayment > self.loan_amount:
            raise ValueError
        self._overpayment = overpayment

    @property
    def overpayment_type(self):
        return self._overpayment_type

    @overpayment_type.setter
    def overpayment_type(self, overpayment_type):
        if overpayment_type not in ['one-time', 'monthly']:
            raise ValueError
        self._overpayment_type = overpayment_type

    def calculate_monthly_payment(self):
        if self.installments_type == 'equal':
            sigma = 0
            i = 1
            while i <= self.period_in_months:
                sigma += (1 + self.nominal_rate / 100 / 12) ** (-i)
                i += 1
            monthly_payment = self.loan_amount / sigma
            return round(monthly_payment, 2)

        elif self.installments_type == 'decreasing':
            first_month_payment = self.loan_amount / self.period_in_months * \
                                  (1 + (self.period_in_months * self.nominal_rate / 100 / 12))
            return round(first_month_payment, 2)

    def calculate_all_installments(self):
        if self.installments_type == 'equal':
            return [self.monthly_payment] * self.period_in_months

        elif self.installments_type == 'decreasing':
            all_installments = []
            for month in reversed(range(1, self.period_in_months + 1)):
                installment = self.loan_amount / self.period_in_months * (1 + (month * self.nominal_rate / 100 / 12))
                all_installments.append(round(installment, 2))
            return all_installments

    def calculate_remaining(self):
        remaining = [round(self.total_amount - self.all_installments[0], 2)]
        for i in range(0, len(self.all_installments)-1):
            remaining.append(round(remaining[i]-self.all_installments[i+1], 2))

        return remaining

    def generate_payment_schedule(self):
        data = {'Installments': self.all_installments,
                'Remaining': self.remaining}
        row_labels = range(1, self.period_in_months+1)
        return pd.DataFrame(data=data, index=row_labels)

    def calculate_total_amount(self):
        return sum(self.all_installments)

    def calculate_total_interest(self):
        return self.total_amount - self.loan_amount


def save_schedule_to_csv(path_to_save):
    mortgage.payment_schedule.to_csv(path_to_save)


if __name__ == '__main__':
    args = parser.parse_args()

    mortgage = Mortgage(args.loan, args.rate, args.months, args.installments, args.overpayment, args.overpayment_type)

    print("Total amount: " + str(mortgage.total_amount))
    print("Total interest: " + str(mortgage.total_interest))
    print("Monthly payment: " + str(mortgage.monthly_payment))
    print("All installments:\n" + str(mortgage.all_installments))
    print("Remaining:\n" + str(mortgage.remaining))
    print("Payment schedule:\n" + str(mortgage.payment_schedule))

    save_schedule_to_csv("Payment_schedule.csv")
