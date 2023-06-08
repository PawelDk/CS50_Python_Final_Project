import project
import pytest
import pandas as pd


TEST_LOAN_1e = 50000
TEST_RATE_1e = 7
TEST_MONTHS_1e = 60
TEST_INSTALLMENTS_1e = 'equal'
TEST_OVERPAYMENT_1e = 5000
TEST_LOAN_1d = 50000
TEST_RATE_1d = 7
TEST_MONTHS_1d = 60
TEST_INSTALLMENTS_1d = 'decreasing'
TEST_OVERPAYMENT_1d = 5000


@pytest.fixture
def mortgage_equal():
    return project.Mortgage(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e, TEST_OVERPAYMENT_1e)

@pytest.fixture
def mortgage_decreasing():
    return project.Mortgage(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d, TEST_OVERPAYMENT_1d)


"""
External functions tests.
Testing functions external to the Mortgage class that were required by the CS50 course final project.
"""
@pytest.mark.external_functions_testing
def test_generate_mortgage_sheet():
    """
    Happy paths of generate_mortgage_sheet function,
    with and without overpayment, for both type of installments [equal, decreasing].
    """
    # Without overpayment - equal
    data = {'Mortgage attributes sheet': [float(TEST_LOAN_1e), float(TEST_RATE_1e), TEST_MONTHS_1e, TEST_INSTALLMENTS_1e]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_attributes_sheet(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e,
                                                            TEST_INSTALLMENTS_1e)

    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # Without overpayment - decreasing
    data = {'Mortgage attributes sheet': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_attributes_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d,
                                                            TEST_INSTALLMENTS_1d)

    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # With overpayment - equal
    data = {'Mortgage attributes sheet': [float(TEST_LOAN_1e), float(TEST_RATE_1e), TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                          '------', float(TEST_OVERPAYMENT_1e)]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments',
                  '---', 'Overpayment']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_attributes_sheet(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                                            TEST_OVERPAYMENT_1e)
    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

    # With overpayment - decreasing
    data = {'Mortgage attributes sheet': [float(TEST_LOAN_1d), float(TEST_RATE_1d), TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                          '------', float(TEST_OVERPAYMENT_1d)]}
    row_labels = ['Loan amount', 'Nominal interest rate, %', 'Repayment period, months', 'Type of installments',
                  '---', 'Overpayment']
    test_sheet_to_compare = pd.DataFrame(data=data, index=row_labels)

    test_sheet = project.generate_mortgage_attributes_sheet(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                                            TEST_OVERPAYMENT_1d)
    assert isinstance(test_sheet, pd.DataFrame)
    if isinstance(test_sheet, pd.DataFrame):
        assert test_sheet.compare(test_sheet_to_compare).empty

@pytest.mark.external_functions_testing
def test_calculate_overpayment_saving():
    """
    Happy paths of calculate_overpayment_saving function, for both type of installments [equal, decreasing].
    """

    to_compare_equal = 940.6
    result_equal = project.calculate_overpayment_saving(TEST_LOAN_1e, TEST_RATE_1e, TEST_MONTHS_1e, TEST_INSTALLMENTS_1e,
                                                        TEST_OVERPAYMENT_1e)
    assert result_equal == to_compare_equal

    to_compare_decreasing = 889.61
    result_decreasing = project.calculate_overpayment_saving(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d, TEST_INSTALLMENTS_1d,
                                                             TEST_OVERPAYMENT_1d)
    assert result_decreasing == to_compare_decreasing

@pytest.mark.external_functions_testing
def test_calculate_decreasing_installments_saving():
    """
    Happy path of calculate_decreasing_installments_saving function.
    Type of installments [equal, decreasing] does not affect these calculations - hence only one assert.
    """

    to_compare_decreasing = 507.76
    result_decreasing = project.calculate_decreasing_installments_saving(TEST_LOAN_1d, TEST_RATE_1d, TEST_MONTHS_1d)
    assert result_decreasing == to_compare_decreasing


"""
Main functionalities tests.
Testing results of all calculations performed to populate output sheets: calculation summary and payment schedules 
"""

@pytest.mark.external_functions_testing
def test_total_amount_to_be_repaid_equal(mortgage_equal):
    assert mortgage_equal.total_amount == 59403.6

@pytest.mark.external_functions_testing
def test_total_amount_to_be_repaid_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.total_amount == 58895.84

@pytest.mark.external_functions_testing
def test_total_interest_equal(mortgage_equal):
    assert mortgage_equal.total_interest == 9403.6

@pytest.mark.external_functions_testing
def test_total_interest_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.total_interest == 8895.84

@pytest.mark.external_functions_testing
def test_monthly_payment_equal(mortgage_equal):
    assert mortgage_equal.monthly_payment == 990.06

@pytest.mark.external_functions_testing
def test_monthly_payment_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.monthly_payment == 1125.00

@pytest.mark.external_functions_testing
def test_overpayment_saving_equal(mortgage_equal):
    assert mortgage_equal.overpayment_saving == 940.6

@pytest.mark.external_functions_testing
def test_overpayment_saving_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.overpayment_saving == 889.61

@pytest.mark.external_functions_testing
def test_new_total_amount_to_be_repaid_equal(mortgage_equal):
    assert mortgage_equal.new_total_amount == 53463.0

@pytest.mark.external_functions_testing
def test_new_total_amount_to_be_repaid_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_total_amount == 53006.23

@pytest.mark.external_functions_testing
def test_new_total_interest_equal(mortgage_equal):
    assert mortgage_equal.new_total_interest == 8463.0

@pytest.mark.external_functions_testing
def test_new_total_interest_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_total_interest == 8006.23

@pytest.mark.external_functions_testing
def test_new_monthly_payment_equal(mortgage_equal):
    assert mortgage_equal.new_monthly_payment == 891.05

@pytest.mark.external_functions_testing
def test_new_monthly_payment_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_monthly_payment == 1012.5
