import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--loan', '-l', help="Loan amount, USD", type=int)
parser.add_argument('--rate', '-r', help="Nominal interest rate (per year), %", type=int)
parser.add_argument('--months', '-m', help="Repayment period, months", type=int)
parser.add_argument('--inst', '-i', help="Type of installments [equal, decreasing]", type=str)


def monthly_payment_equal(loan, r, p):
    sigma = 0
    i = 1
    while i <= p:
        sigma += (1 + r/100/12) ** (-i)
        i += 1

    return loan / sigma

def monthly_payment_decreasing(loan, r, m):
    schedule = []
    for n in reversed(range(1, m+1)):
        print(n)
        installment = loan/m * (1 + (n * r/100/12))
        print(installment)
        schedule.append(installment)

    return schedule


if __name__ == '__main__':
    args = parser.parse_args()
    # print("Installment: " + str(monthly_payment_equal(args.loan, args.rate, args.months)))
    print("Installment: " + str(monthly_payment_decreasing(args.loan, args.rate, args.months)))

