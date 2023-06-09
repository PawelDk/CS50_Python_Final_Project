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
def test_generate_mortgage_attributes_sheet():
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

@pytest.mark.main_functionalities_testing
def test_total_amount_to_be_repaid_equal(mortgage_equal):
    assert mortgage_equal.total_amount == 59403.6

@pytest.mark.main_functionalities_testing
def test_total_amount_to_be_repaid_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.total_amount == 58895.84

@pytest.mark.main_functionalities_testing
def test_total_interest_equal(mortgage_equal):
    assert mortgage_equal.total_interest == 9403.6

@pytest.mark.main_functionalities_testing
def test_total_interest_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.total_interest == 8895.84

@pytest.mark.main_functionalities_testing
def test_monthly_payment_equal(mortgage_equal):
    assert mortgage_equal.monthly_payment == 990.06

@pytest.mark.main_functionalities_testing
def test_monthly_payment_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.monthly_payment == 1125.00

@pytest.mark.main_functionalities_testing
def test_overpayment_saving_equal(mortgage_equal):
    assert mortgage_equal.overpayment_saving == 940.6

@pytest.mark.main_functionalities_testing
def test_overpayment_saving_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.overpayment_saving == 889.61

@pytest.mark.main_functionalities_testing
def test_new_total_amount_to_be_repaid_equal(mortgage_equal):
    assert mortgage_equal.new_total_amount == 53463.0

@pytest.mark.main_functionalities_testing
def test_new_total_amount_to_be_repaid_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_total_amount == 53006.23

@pytest.mark.main_functionalities_testing
def test_new_total_interest_equal(mortgage_equal):
    assert mortgage_equal.new_total_interest == 8463.0

@pytest.mark.main_functionalities_testing
def test_new_total_interest_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_total_interest == 8006.23

@pytest.mark.main_functionalities_testing
def test_new_monthly_payment_equal(mortgage_equal):
    assert mortgage_equal.new_monthly_payment == 891.05

@pytest.mark.main_functionalities_testing
def test_new_monthly_payment_decreasing(mortgage_decreasing):
    assert mortgage_decreasing.new_monthly_payment == 1012.5


"""
Exception handling tests.
Testing behavior of the system in case of incorrect input data
"""

@pytest.mark.exception_handling_testing_external_functions
def test_generate_mortgage_attributes_sheet_input_missing():
    common_part = "generate_mortgage_attributes_sheet() missing 1 required positional argument: "

    with pytest.raises(TypeError) as message:
        project.generate_mortgage_attributes_sheet(months=TEST_MONTHS_1e, rate=TEST_RATE_1e,
                                                   installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'loan'"

    with pytest.raises(TypeError) as message:
        project.generate_mortgage_attributes_sheet(loan=TEST_LOAN_1e, months=TEST_MONTHS_1e,
                                                   installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'rate'"

    with pytest.raises(TypeError) as message:
        project.generate_mortgage_attributes_sheet(loan=TEST_LOAN_1e, rate=TEST_RATE_1e,
                                                   installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'months'"

    with pytest.raises(TypeError) as message:
        project.generate_mortgage_attributes_sheet(loan=TEST_LOAN_1e, months=TEST_MONTHS_1e, rate=TEST_RATE_1e)
    assert message.value.args[0] == common_part + "'installments'"

@pytest.mark.exception_handling_testing_external_functions
def test_calculate_overpayment_saving_input_missing():
    common_part = "calculate_overpayment_saving() missing 1 required positional argument: "

    with pytest.raises(TypeError) as message:
        project.calculate_overpayment_saving(months=TEST_MONTHS_1e, rate=TEST_RATE_1e,
                                             installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'loan'"

    with pytest.raises(TypeError) as message:
        project.calculate_overpayment_saving(loan=TEST_LOAN_1e, months=TEST_MONTHS_1e,
                                             installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'rate'"

    with pytest.raises(TypeError) as message:
        project.calculate_overpayment_saving(loan=TEST_LOAN_1e, rate=TEST_RATE_1e,
                                             installments=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'months'"

    with pytest.raises(TypeError) as message:
        project.calculate_overpayment_saving(loan=TEST_LOAN_1e, months=TEST_MONTHS_1e, rate=TEST_RATE_1e)
    assert message.value.args[0] == common_part + "'installments'"

@pytest.mark.exception_handling_testing_external_functions
def test_calculate_decreasing_installments_saving_input_missing():
    common_part = "calculate_decreasing_installments_saving() missing 1 required positional argument: "

    with pytest.raises(TypeError) as message:
        project.calculate_decreasing_installments_saving(months=TEST_MONTHS_1e, rate=TEST_RATE_1e)
    assert message.value.args[0] == common_part + "'loan'"

    with pytest.raises(TypeError) as message:
        project.calculate_decreasing_installments_saving(loan=TEST_LOAN_1e, months=TEST_MONTHS_1e)
    assert message.value.args[0] == common_part + "'rate'"

    with pytest.raises(TypeError) as message:
        project.calculate_decreasing_installments_saving(loan=TEST_LOAN_1e, rate=TEST_RATE_1e)
    assert message.value.args[0] == common_part + "'months'"

@pytest.mark.exception_handling_testing_object_init
def test_all_object_inputs_missing():
    with pytest.raises(TypeError) as message:
        project.Mortgage()
    assert message.value.args[0] == "__init__() missing 4 required positional arguments: 'loan_amount', " \
                                    "'nominal_rate', 'period_in_months', and 'installments_type'"

@pytest.mark.exception_handling_testing_object_init
def test_one_object_input_missing():
    common_part = "__init__() missing 1 required positional argument: "

    with pytest.raises(TypeError) as message:
        project.Mortgage(period_in_months=TEST_MONTHS_1e, nominal_rate=TEST_RATE_1e, installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'loan_amount'"

    with pytest.raises(TypeError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, period_in_months=TEST_MONTHS_1e, installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'nominal_rate'"

    with pytest.raises(TypeError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == common_part + "'period_in_months'"

    with pytest.raises(TypeError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, period_in_months=TEST_MONTHS_1e, nominal_rate=TEST_RATE_1e)
    assert message.value.args[0] == common_part + "'installments_type'"

@pytest.mark.exception_handling_testing_wrong_format
def test_wrong_format_given_loan():
    correct_message = "Wrong loan amount format given. Please use float or int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount='some_string', nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_wrong_format
def test_wrong_format_given_rate():
    correct_message = "Wrong nominal rate format given. Please use float or int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate='some_string', period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_wrong_format
def test_wrong_format_given_months():
    correct_message = "Wrong period in months format given. Please use int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months='some_string',
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=123.456,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_wrong_format
def test_wrong_format_given_installments():
    correct_message = "Wrong installments type format given. Please use string out of: 'equal', 'decreasing'.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=123)
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=123.456)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_wrong_format
def test_wrong_format_given_overpayment():
    correct_message = "Wrong overpayment format given. Please use float or int value greater than 0 and less than or " \
                      "equal to the amount of the loan.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e, overpayment='some_string')
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_loan_less_than_or_equal_to_0():
    correct_message = "An incorrect loan amount was given. Please use float or int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=-1000000, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=0, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_rate_less_than_or_equal_to_0():
    correct_message = "An incorrect nominal rate was given. Please use float or int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=-5, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=0, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_months_less_than_or_equal_to_0():
    correct_message = "An incorrect period in months was given. Please use int value greater than 0.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=-5,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=0,
                         installments_type=TEST_INSTALLMENTS_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_overpayment_less_than_0():
    # overpayment=0 will not raise ValueError because it will be treated like None
    correct_message = "An incorrect value of overpayment was given. Please use float or int value greater than 0 and" \
                      " less than or equal to the amount of the loan.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e, overpayment=-500)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_overpayment_more_than_loan():
    correct_message = "An incorrect value of overpayment was given. Please use float or int value greater than 0 and" \
                      " less than or equal to the amount of the loan.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type=TEST_INSTALLMENTS_1e, overpayment=2*TEST_LOAN_1e)
    assert message.value.args[0] == correct_message

@pytest.mark.exception_handling_testing_logically_incorrect_input
def test_installments_out_of_list():
    correct_message = "An incorrect input for installments type was given. Please use string out of: 'equal'," \
                      " 'decreasing'.\n\n"

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type='decr')
    assert message.value.args[0] == correct_message

    with pytest.raises(ValueError) as message:
        project.Mortgage(loan_amount=TEST_LOAN_1e, nominal_rate=TEST_RATE_1e, period_in_months=TEST_MONTHS_1e,
                         installments_type='EQUAL')
    assert message.value.args[0] == correct_message
