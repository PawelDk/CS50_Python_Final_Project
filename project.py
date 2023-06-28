import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--loan', '-l', help="Loan amount, USD", type=float)
parser.add_argument('--rate', '-r', help="Nominal interest rate (per year), %", type=float)
parser.add_argument('--months', '-m', help="Repayment period, months", type=int)
parser.add_argument('--installments', '-i', help="Type of installments [equal, decreasing]", type=str)
parser.add_argument('--overpayment', '-o', help="Overpayment value, USD (optional)", type=float)

class Mortgage:
    INSTALLMENTS_TYPE_EQUAL = 'equal'
    INSTALLMENTS_TYPE_DECREASING = 'decreasing'
    VALUE_ERROR_MESSAGES = {
        'loan_amount': "===========   An incorrect loan amount was given. Please use float or int value greater than "
                       "0.\n\n",
        'nominal_rate': "===========   An incorrect nominal rate was given. Please use float or int value greater "
                        "than 0.\n\n",
        'period_in_months': "===========   An incorrect period in months was given. Please use int value greater than "
                            "0.\n\n",
        'installments_type': "===========   An incorrect input for installments type was given. Please use string out "
                             "of: 'equal', 'decreasing'.\n\n",
        'overpayment': "===========   Incorrect value of overpayment was given. Please use float or int value "
                       "greater than 0 and less than or equal to the amount of the loan.\n\n",
        'no_loan_amount': "===========   No loan amount was given. Please use float or int value greater than 0.\n\n",
        'no_nominal_rate': "===========   No nominal rate was given. Please use float or int value greater than 0.\n\n",
        'no_period_in_months': "===========   No period in months was given. Please use int value greater than 0.\n\n",
        'no_installments_type': "===========   No input for installments type was given. Please use string out of:"
                                " 'equal', 'decreasing'.\n\n",
        'loan_amount_wrong_format': "===========   Wrong loan amount format given. Please use float or int value "
                                    "greater than 0.\n\n",
        'nominal_rate_wrong_format': "===========   Wrong nominal rate format given. Please use float or int value "
                                    "greater than 0.\n\n",
        'period_in_months_wrong_format': "===========   Wrong period in months format given. Please use int value "
                                    "greater than 0.\n\n",
        'installments_type_wrong_format': "===========   Wrong installments type format given. Please use string out "
                                          "of: 'equal', 'decreasing'.\n\n",
        'overpayment_wrong_format': "===========   Wrong overpayment format given. Please use float or int value "
                                    "greater than 0 and less than or equal to the amount of the loan.\n\n"}

    def __init__(self, loan_amount, nominal_rate, period_in_months, installments_type,
                 overpayment=None):
        self.loan_amount = loan_amount
        self.nominal_rate = nominal_rate
        self.period_in_months = period_in_months
        self.installments_type = installments_type
        self.overpayment = overpayment

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
        if self.overpayment:
            self.overpayment_saving = self.calculate_overpayment_saving()

        self.mortgage_attributes_sheet = self.generate_mortgage_attributes_sheet()
        self.calculation_summary = self.generate_calculation_summary()
        self.payment_schedule = self.generate_payment_schedule()
        if self.overpayment:
            self.payment_schedule_with_overpayment = self.generate_payment_schedule_with_overpayment()

        pd.options.display.float_format = '{:.2f}'.format

    @property
    def loan_amount(self):
        return self._loan_amount

    @loan_amount.setter
    def loan_amount(self, loan_amount):
        if loan_amount:
            if isinstance(loan_amount, float) or isinstance(loan_amount, int):
                if loan_amount <= 0:
                    raise ValueError(self.VALUE_ERROR_MESSAGES['loan_amount'])
                self._loan_amount = loan_amount
            else:
                raise ValueError(self.VALUE_ERROR_MESSAGES['loan_amount_wrong_format'])
        else:
            raise ValueError(self.VALUE_ERROR_MESSAGES['no_loan_amount'])

    @property
    def nominal_rate(self):
        return self._nominal_rate

    @nominal_rate.setter
    def nominal_rate(self, nominal_rate):
        if nominal_rate:
            if isinstance(nominal_rate, float) or isinstance(nominal_rate, int):
                if nominal_rate <= 0:
                    raise ValueError(self.VALUE_ERROR_MESSAGES['nominal_rate'])
                self._nominal_rate = nominal_rate
            else:
                raise ValueError(self.VALUE_ERROR_MESSAGES['nominal_rate_wrong_format'])
        else:
            raise ValueError(self.VALUE_ERROR_MESSAGES['no_nominal_rate'])

    @property
    def period_in_months(self):
        return self._period_in_months

    @period_in_months.setter
    def period_in_months(self, period_in_months):
        if period_in_months:
            if isinstance(period_in_months, int):
                if period_in_months <= 0:
                    raise ValueError(self.VALUE_ERROR_MESSAGES['period_in_months'])
                self._period_in_months = period_in_months
            else:
                raise ValueError(self.VALUE_ERROR_MESSAGES['period_in_months_wrong_format'])
        else:
            raise ValueError(self.VALUE_ERROR_MESSAGES['no_period_in_months'])

    @property
    def installments_type(self):
        return self._installments_type

    @installments_type.setter
    def installments_type(self, installments_type):
        if installments_type:
            if isinstance(installments_type, str):
                if installments_type not in [self.INSTALLMENTS_TYPE_EQUAL, self.INSTALLMENTS_TYPE_DECREASING]:
                    raise ValueError(self.VALUE_ERROR_MESSAGES['installments_type'])
                self._installments_type = installments_type
            else:
                raise ValueError(self.VALUE_ERROR_MESSAGES['installments_type_wrong_format'])
        else:
            raise ValueError(self.VALUE_ERROR_MESSAGES['no_installments_type'])

    @property
    def overpayment(self):
        return self._overpayment

    @overpayment.setter
    def overpayment(self, overpayment):
        if overpayment:
            if isinstance(overpayment, float) or isinstance(overpayment, int):
                if overpayment <= 0 or overpayment > self.loan_amount:
                    raise ValueError(self.VALUE_ERROR_MESSAGES['overpayment'])
                self._overpayment = overpayment
            else:
                raise ValueError(self.VALUE_ERROR_MESSAGES['overpayment_wrong_format'])
        else:
            self._overpayment = overpayment

    def calculate_loan_characteristics(self):
        """
        Calling methods that calculate loan characteristics before and after overpayment.
        """
        # all characteristics
        self.monthly_payment = self.calculate_monthly_payment(if_overpayment=False)
        self.all_installments = self.calculate_all_installments(if_overpayment=False)
        self.total_amount = self.calculate_total_amount(if_overpayment=False)
        self.total_interest = self.calculate_total_interest(if_overpayment=False)
        self.remaining = self.calculate_remaining(if_overpayment=False)

        # all characteristics updated by overpayment
        if self.overpayment:
            self.new_monthly_payment = self.calculate_monthly_payment(if_overpayment=True)
            self.new_all_installments = self.calculate_all_installments(if_overpayment=True)
            self.new_total_amount = self.calculate_total_amount(if_overpayment=True)
            self.new_total_interest = self.calculate_total_interest(if_overpayment=True)
            self.new_remaining = self.calculate_remaining(if_overpayment=True)

    def calculate_monthly_payment(self, if_overpayment):
        """
        Calculating one of loan characteristics - monthly payment
        """
        if if_overpayment:
            overpayment = self.overpayment
        else:
            overpayment = 0

        if self.installments_type == self.INSTALLMENTS_TYPE_EQUAL:
            sigma = 0
            i = 1
            while i <= self.period_in_months:
                sigma += (1 + self.nominal_rate / 100 / 12) ** (-i)
                i += 1
            monthly_payment = (self.loan_amount - overpayment) / sigma
            return round(monthly_payment, 2)

        elif self.installments_type == self.INSTALLMENTS_TYPE_DECREASING:
            first_month_payment = (self.loan_amount - overpayment) / self.period_in_months * \
                                  (1 + (self.period_in_months * self.nominal_rate / 100 / 12))
            return round(first_month_payment, 2)

    def calculate_all_installments(self, if_overpayment):
        """
        Calculating one of loan characteristics - all installments
        """
        if if_overpayment:
            monthly_payment = self.new_monthly_payment
            overpayment = self.overpayment
        else:
            monthly_payment = self.monthly_payment
            overpayment = 0

        if self.installments_type == self.INSTALLMENTS_TYPE_EQUAL:
            return [monthly_payment] * self.period_in_months

        elif self.installments_type == self.INSTALLMENTS_TYPE_DECREASING:
            all_installments = []
            for month in reversed(range(1, self.period_in_months + 1)):
                installment = (self.loan_amount - overpayment) / self.period_in_months * \
                              (1 + (month * self.nominal_rate / 100 / 12))
                all_installments.append(round(installment, 2))
            return all_installments

    def calculate_total_amount(self, if_overpayment):
        """
        Calculating one of loan characteristics - total amount
        """
        if if_overpayment:
            return round(sum(self.new_all_installments), 2)
        else:
            return round(sum(self.all_installments), 2)

    def calculate_total_interest(self, if_overpayment):
        """
        Calculating one of loan characteristics - total interest
        """
        if if_overpayment:
            return round(self.new_total_amount - (self.loan_amount - self.overpayment), 2)
        else:
            return round(self.total_amount - self.loan_amount, 2)

    def calculate_remaining(self, if_overpayment):
        """
        Calculating one of loan characteristics - remainig
        """
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
        """
        Calculating overpayment saving.
        """
        return round(self.total_interest - self.new_total_interest, 2)

    def generate_mortgage_attributes_sheet(self):
        """
        The method returns a DataFrame with input loan parameters.
        """
        all_data = [self.loan_amount, self.nominal_rate, self.period_in_months, self.installments_type]
        row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
        if self.overpayment:
            all_data += ['------', self.overpayment]
            row_labels += ['---', 'Overpayment']

        data = {'Mortgage attributes sheet': all_data}

        return pd.DataFrame(data=data, index=row_labels)

    def generate_calculation_summary(self):
        """
        The method returns a DataFrame with loan characteristics calculated based on input parameters.
        """
        all_data = [self.total_amount, self.total_interest, self.monthly_payment]
        row_labels = ['Total amount to be repaid', 'Total interest', 'Monthly payment']
        if self.overpayment:
            all_data += ['------', self.overpayment_saving, self.new_total_amount, self.new_total_interest, self.new_monthly_payment]
            row_labels += ['---', 'Overpayment saving', 'New total amount to be repaid', 'New total interest', 'New monthly payment', ]
        data = {'Calculation result': all_data}

        return pd.DataFrame(data=data, index=row_labels)

    def generate_payment_schedule(self):
        """
        The method returns a DataFrame with calculated payment schedule (not including overpayment).
        """
        data = {'Installments': self.all_installments,
                'Remaining': self.remaining}
        row_labels = range(1, self.period_in_months+1)
        return pd.DataFrame(data=data, index=row_labels)

    def generate_payment_schedule_with_overpayment(self):
        """
        The method returns a DataFrame with calculated payment schedule (including overpayment).
        """
        new_df = self.payment_schedule.copy(deep=True)
        new_df['New installments'] = self.new_all_installments
        new_df['New remaining'] = self.new_remaining
        return new_df[['Installments','New installments','Remaining','New remaining']]

    def save_schedule_to_csv(self, path_to_save):
        """
        Saving payment schedule to csv file.
        """
        self.payment_schedule.to_csv(path_to_save)
        if self.overpayment:
            self.payment_schedule_with_overpayment.to_csv(path_to_save[:-4] + "_with_overpayment.csv")


def generate_mortgage_attributes_sheet(loan=None, rate=None, months=None, installments=None, overpayment=None):
    """
    :return: Using the Mortgage class, the function generates a mortgage attributes sheet.
    """
    mortgage_to_calculate = Mortgage(loan_amount=loan, nominal_rate=rate, period_in_months=months,
                                     installments_type=installments, overpayment=overpayment)
    return mortgage_to_calculate.mortgage_attributes_sheet

def calculate_overpayment_saving(loan=None, rate=None, months=None, installments=None, overpayment=None):
    """
    :return: Using the Mortgage class, the function calculates total savings resulting from the overpayment.
    """
    mortgage_to_calculate = Mortgage(loan_amount=loan, nominal_rate=rate, period_in_months=months,
                                     installments_type=installments, overpayment=overpayment)
    return mortgage_to_calculate.overpayment_saving

def calculate_decreasing_installments_saving(loan=None, rate=None, months=None):
    """
    :return: Using the Mortgage class, the function calculates savings resulting from the choice of decreasing
    installments.
    """
    mortgage_to_calculate_equal = Mortgage(loan_amount=loan, nominal_rate=rate, period_in_months=months,
                                           installments_type='equal')
    mortgage_to_calculate_decreasing = Mortgage(loan_amount=loan, nominal_rate=rate, period_in_months=months,
                                                installments_type='decreasing')
    return round(mortgage_to_calculate_equal.total_interest - mortgage_to_calculate_decreasing.total_interest, 2)

def main():
    args = parser.parse_args()

    """
    # for debug
    args.loan = 50000
    args.rate = 7
    args.months = 50
    args.installments = 'decreasing'
    args.overpayment = 2000
    """

    mortgage = Mortgage(args.loan, args.rate, args.months, args.installments, args.overpayment)

    print(mortgage.mortgage_attributes_sheet)
    print()
    print(mortgage.calculation_summary)
    print()
    print(mortgage.payment_schedule)
    print()
    if mortgage.overpayment:
        print(mortgage.payment_schedule_with_overpayment)
    print()

    mortgage.save_schedule_to_csv("Payment_schedule.csv")

    print("--- Additional functions usages ---: ")
    print("calculate_mortgage_attributes_sheet: ")
    if mortgage.overpayment:
        print(generate_mortgage_attributes_sheet(args.loan, args.rate, args.months, args.installments, args.overpayment))
    else:
        print(generate_mortgage_attributes_sheet(args.loan, args.rate, args.months, args.installments))

    if mortgage.overpayment:
        print("calculate_overpayment_saving: ")
        print(calculate_overpayment_saving(args.loan, args.rate, args.months, args.installments, args.overpayment))

    print("calculate_decreasing_installments_saving: ")
    print(calculate_decreasing_installments_saving(args.loan, args.rate, args.months))


if __name__ == '__main__':
    main()
