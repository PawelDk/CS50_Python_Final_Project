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
TEST_INSTALLMENTS_1e = 'equal'
TEST_OVERPAYMENT_1e = 45000

@pytest.fixture
def mortgage():
    return project.Mortgage(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d)

# Testing custom function outside of Mortgage class:
def test_generate_mortgage_sheet(mortgage):
    """
    Happy paths of generate_mortgage_sheet function,
    with and without overpayment, for both type of installments [equal, decreasing].
    """
    # Without overpayment - equal
    data = {'Mortgage attributes': [float(TEST_LOAN_1e), float(TEST_RATE_1e), TEST_MONTHS_1e, TEST_INSTALLMENTS_1e]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_sheet(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e)

    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # Without overpayment - decreasing
    data = {'Mortgage attributes': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d)

    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # With overpayment - equal
    data = {'Mortgage attributes': [float(TEST_LOAN_1e), float(TEST_RATE_1e), TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                    '------', float(TEST_OVERPAYMENT_1e)]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments',
                  '---', 'Overpayment']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_sheet(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                                 TEST_OVERPAYMENT_1e)
    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # With overpayment - decreasing
    data = {'Mortgage attributes': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                    '------', float(TEST_OVERPAYMENT_1d)]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments',
                  '---', 'Overpayment']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                                 TEST_OVERPAYMENT_1d)
    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

def test_calculate_overpayment_saving():
    """
    Happy paths of calculate_overpayment_saving function, for both type of installments [equal, decreasing].
    """

    to_compare_equal = 8463.0
    result_equal = project.calculate_overpayment_saving(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                                        TEST_OVERPAYMENT_1e)
    assert result_equal == to_compare_equal

    to_compare_decreasing = 8006.27
    result_decreasing = project.calculate_overpayment_saving(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                                             TEST_OVERPAYMENT_1d)
    assert result_decreasing == to_compare_decreasing

def test_calculate_decreasing_installments_saving():
    """
    Happy path of calculate_decreasing_installments_saving function.
    Type of installments [equal, decreasing] does not affect these calculations - hence only one assert.
    """

    to_compare_decreasing = 507.76
    result_decreasing = project.calculate_decreasing_installments_saving(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d)
    assert result_decreasing == to_compare_decreasing

# Main functionalities tests:
def test_monthly_payment(mortgage):
    """
    Happy path of class, no overpayment.
    """
    assert mortgage.monthly_payment == 1125.00
