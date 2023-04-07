from project import Mortgage
import pytest

TEST_LOAN = 50000
TEST_RATE = 7
TEST_MONTHS = 60
TEST_INSTALLMENTS = 'decreasing'
TEST_OVERPAYMENT = 45000

@pytest.fixture
def mortgage():
    return Mortgage(TEST_LOAN, TEST_RATE, TEST_MONTHS, TEST_INSTALLMENTS)

def test_monthly_payment(mortgage):
    assert mortgage.monthly_payment == 1125.00

