def calculate_saving_rate() -> None:
    starting_salary: float = float(input("Please enter your starting salary: "))

    total_cost: float = 1000000
    portion_down_payment: float = total_cost * 0.25

    epsilon: float = 100

    # Calculate if possible to save with 100% of money first
    total_savings = calculate_three_year_savings(starting_salary, 1.0)

    if total_savings < portion_down_payment:
        print("It is not possible to save for a down payment in 36 months.")
        return

    # Calculate best saving rate using bisection search
    low: float = 0
    high: float = 10000
    num_guesses: int = 0

    while True:
        guess = (low + high) / 2.0
        savings_rate = guess / 10000

        total_savings = calculate_three_year_savings(starting_salary, savings_rate)

        num_guesses += 1
        if abs(total_savings - portion_down_payment) <= epsilon:
            print("Best savings rate:", round(savings_rate, 4))
            print("Number of searches:", num_guesses)
            break
        elif low == high:
            break
        elif total_savings < portion_down_payment:
            low = guess
        elif total_savings > portion_down_payment:
            high = guess


def calculate_three_year_savings(starting_salary: float, savings_rate: float):
    current_savings: float = 0
    annual_salary: float = starting_salary
    annual_interest_rate: float = 0.04
    semi_annual_raise: float = 0.07

    for month in range(1, 37):
        current_savings += current_savings * annual_interest_rate / 12
        current_savings += annual_salary / 12 * savings_rate
        if month % 6 == 0:
            annual_salary *= 1 + semi_annual_raise

    return current_savings


if __name__ == "__main__":
    calculate_saving_rate()
