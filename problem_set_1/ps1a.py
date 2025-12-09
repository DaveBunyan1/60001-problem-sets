def calculate_months_for_down_payment() -> None:
    annual_salary: float = float(input("Please enter your annual salary: "))
    portion_saved: float = float(
        input("Please enter the percent of your salary to save, as a decimal: ")
    )
    total_cost: float = float(input("Please enter the cost of your dream home: "))

    portion_down_payment: float = total_cost * 0.25
    current_savings: float = 0.0

    number_of_months: int = 0

    annual_interest_rate: float = 0.04

    while current_savings < portion_down_payment:
        number_of_months += 1
        current_savings += (
            current_savings * annual_interest_rate / 12
            + annual_salary * portion_saved / 12
        )

    print("Number of months:", number_of_months)


if __name__ == "__main__":
    calculate_months_for_down_payment()
