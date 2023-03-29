import argparse
import pandas as pd

INSTALLMENTS_TYPE_EQUAL = 'equal'
INSTALLMENTS_TYPE_DECREASING = 'decreasing'
OVERPAYMENT_TYPE_ONE_TIME = 'one-time'
OVERPAYMENT_TYPE_MONTHLY = 'monthly'

parser = argparse.ArgumentParser()
parser.add_argument('--loan', '-l', help="Loan amount, USD", type=int)
parser.add_argument('--rate', '-r', help="Nominal interest rate (per year), %", type=int)
parser.add_argument('--months', '-m', help="Repayment period, months", type=int)
parser.add_argument('--installments', '-i', help="Type of installments [equal, decreasing]", type=str)
parser.add_argument('--overpayment', '-o', help="Overpayment value, USD", type=float)
parser.add_argument('--overpayment_type', '-ot', help="Overpayment type [one-time, monthly]", type=str)

class Mortgage:
    def __init__(self, loan_amount, nominal_rate, period_in_months, installments_type,
                 overpayment=None, overpayment_type=None):
        self.loan_amount = float(loan_amount)
        self.nominal_rate = float(nominal_rate)
        self.period_in_months = period_in_months
        self.installments_type = installments_type
        self.overpayment = overpayment
        self.overpayment_type = overpayment_type

        self.monthly_payment = None
        self.all_installments = None
        self.total_amount = None
        self.total_interest = None
        self.remaining = None
        self.new_monthly_payment = None
        self.new_all_installments = None
        self.new_total_amount = None
        self.new_total_interest = None
        self.new_remaining = None

        self.calculate_loan_characteristics()
        self.overpayment_saving = self.calculate_overpayment_saving()

        self.mortgage_sheet = self.generate_mortgage_sheet()
        self.calculation_summary = self.generate_calculation_summary()
        self.payment_schedule = self.generate_payment_schedule()
        # todo generate_payment_schedule_with_overpayment_effect()

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
        if installments_type not in [INSTALLMENTS_TYPE_EQUAL, INSTALLMENTS_TYPE_DECREASING]:
            raise ValueError
        self._installments_type = installments_type

    @property
    def overpayment(self):
        return self._overpayment

    @overpayment.setter
    def overpayment(self, overpayment):
        if overpayment:
            if overpayment <= 0 or overpayment > self.loan_amount:
                raise ValueError
            self._overpayment = overpayment

    @property
    def overpayment_type(self):
        return self._overpayment_type

    @overpayment_type.setter
    def overpayment_type(self, overpayment_type):
        if overpayment_type not in [OVERPAYMENT_TYPE_ONE_TIME, OVERPAYMENT_TYPE_MONTHLY, None]:
            raise ValueError
        self._overpayment_type = overpayment_type

    def calculate_loan_characteristics(self):
        # all characteristics
        self.monthly_payment = self.calculate_monthly_payment(if_overpayment=False)
        self.all_installments = self.calculate_all_installments(if_overpayment=False)
        self.total_amount = self.calculate_total_amount(if_overpayment=False)
        self.total_interest = self.calculate_total_interest(if_overpayment=False)
        self.remaining = self.calculate_remaining(if_overpayment=False)

        # all characteristics updated by overpayment
        if self.overpayment:
            if self.overpayment_type == OVERPAYMENT_TYPE_ONE_TIME:
                self.new_monthly_payment = self.calculate_monthly_payment(if_overpayment=True)
                self.new_all_installments = self.calculate_all_installments(if_overpayment=True)
                self.new_total_amount = self.calculate_total_amount(if_overpayment=True)
                self.new_total_interest = self.calculate_total_interest(if_overpayment=True)
                self.new_remaining = self.calculate_remaining(if_overpayment=True)

            elif self.overpayment_type == OVERPAYMENT_TYPE_MONTHLY:
                ...

    def calculate_monthly_payment(self, if_overpayment):
        if if_overpayment:
            overpayment = self.overpayment
        else:
            overpayment = 0

        if self.installments_type == INSTALLMENTS_TYPE_EQUAL:
            sigma = 0
            i = 1
            while i <= self.period_in_months:
                sigma += (1 + self.nominal_rate / 100 / 12) ** (-i)
                i += 1
            monthly_payment = (self.loan_amount - overpayment) / sigma
            return round(monthly_payment, 2)

        elif self.installments_type == INSTALLMENTS_TYPE_DECREASING:
            first_month_payment = (self.loan_amount - overpayment) / self.period_in_months * \
                                  (1 + (self.period_in_months * self.nominal_rate / 100 / 12))
            return round(first_month_payment, 2)

    def calculate_all_installments(self, if_overpayment):
        if if_overpayment:
            monthly_payment = self.new_monthly_payment
            overpayment = self.overpayment
        else:
            monthly_payment = self.monthly_payment
            overpayment = 0

        if self.installments_type == INSTALLMENTS_TYPE_EQUAL:
            return [monthly_payment] * self.period_in_months

        elif self.installments_type == INSTALLMENTS_TYPE_DECREASING:
            all_installments = []
            for month in reversed(range(1, self.period_in_months + 1)):
                installment = (self.loan_amount - overpayment) / self.period_in_months * \
                              (1 + (month * self.nominal_rate / 100 / 12))
                all_installments.append(round(installment, 2))
            return all_installments

    def calculate_total_amount(self, if_overpayment):
        if if_overpayment:
            return round(sum(self.new_all_installments), 2)
        else:
            return round(sum(self.all_installments), 2)

    def calculate_total_interest(self, if_overpayment):
        if if_overpayment:
            return round(self.new_total_amount - (self.loan_amount - self.overpayment), 2)
        else:
            return round(self.total_amount - self.loan_amount, 2)

    def calculate_remaining(self, if_overpayment):
        if if_overpayment:
            remaining = [round(self.new_total_amount - self.new_all_installments[0], 2)]
            for i in range(0, len(self.new_all_installments) - 1):
                remaining.append(round(remaining[i] - self.new_all_installments[i + 1], 2))
        else:
            remaining = [round(self.total_amount - self.all_installments[0], 2)]
            for i in range(0, len(self.all_installments) - 1):
                remaining.append(round(remaining[i] - self.all_installments[i + 1], 2))

        return remaining

    def calculate_overpayment_saving(self):
        return round(self.total_interest - self.new_total_interest, 2)

    def generate_payment_schedule(self):
        data = {'Installments': self.all_installments,
                'Remaining': self.remaining}
        row_labels = range(1, self.period_in_months+1)
        return pd.DataFrame(data=data, index=row_labels)

    def generate_payment_schedule_with_overpayment_effect(self):
        ...

    def generate_mortgage_sheet(self):
        all_data = [self.loan_amount, self.nominal_rate, self.period_in_months, self.installments_type]
        row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
        if self.overpayment:
            all_data += ['------', self.overpayment, self.overpayment_type]
            row_labels += ['---', 'Overpayment', 'Overpayment type']

        data = {'Mortgage attributes': all_data}

        return pd.DataFrame(data=data, index=row_labels)

    def generate_calculation_summary(self):
        all_data = [self.total_amount, self.total_interest, self.monthly_payment]
        row_labels = ['Repayment amount', 'Total interest', 'Monthly payment']
        if self.overpayment:
            all_data += ['------', self.overpayment_saving, self.new_total_amount, self.new_total_interest, self.new_monthly_payment]
            row_labels += ['---', 'Overpayment saving', 'New repayment amount', 'New total interest', 'New monthly payment', ]
        data = {'Calculation result': all_data}

        return pd.DataFrame(data=data, index=row_labels)


def save_schedule_to_csv(path_to_save):
    mortgage.payment_schedule.to_csv(path_to_save)


if __name__ == '__main__':
    args = parser.parse_args()
    """
    for debug
    # args.loan = 50000
    # args.rate = 7
    # args.months = 60
    # args.installments = 'equal'
    # args.overpayment = 100
    # args.overpayment_type = 'one-time'
    """

    mortgage = Mortgage(args.loan, args.rate, args.months, args.installments, args.overpayment, args.overpayment_type)

    print(mortgage.mortgage_sheet)
    print()
    print(mortgage.calculation_summary)
    print()
    print(mortgage.payment_schedule)

    save_schedule_to_csv("Payment_schedule.csv")
