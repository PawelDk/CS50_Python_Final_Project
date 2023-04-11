import project
import pytest
import pandas as pd


TEST_LOAN_1d = 50000
TEST_RATE_1d = 7
TEST_MONTHS_1d = 60
TEST_INSTALLMENTS_1d = 'decreasing'
TEST_OVERPAYMENT_1d = 45000
TEST_LOAN_1e = 50000
TEST_RATE_1e = 7
TEST_MONTHS_1e = 60
TEST_INSTALLMENTS_1e = 'decreasing'
TEST_OVERPAYMENT_1e = 45000

@pytest.fixture
def mortgage():
    return project.Mortgage(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d)

def test_monthly_payment(mortgage):
    """
    Happy path of class, no overpayment.
    """
    assert mortgage.monthly_payment == 1125.00

def test_calculate_mortgage_sheet_no_overpayment(mortgage):
    """
    Happy path of function, no overpayment.
    """
    data = {'Mortgage attributes': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.calculate_mortgage_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d)

    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

def test_calculate_mortgage_sheet_overpayment(mortgage):
    """
    Happy path of function, with overpayment.
    """
    data = {'Mortgage attributes': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                    '------', float(TEST_OVERPAYMENT_1d)]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments',
                  '---', 'Overpayment']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.calculate_mortgage_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                                  TEST_OVERPAYMENT_1d)
    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty



# def calculate_overpayment_saving(loan, rate, months, installments, overpayment):
#
# def calculate_decreasing_installments_saving(loan, rate, months):
#