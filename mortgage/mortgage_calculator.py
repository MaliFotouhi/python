import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the effective interest rate
def calculate_effective_interest_rate(interest_rate, amortization_rate):
    return interest_rate + amortization_rate

# User input for loan, purchase price, and special repayment details
purchase_price = float(input("Enter the property purchase price in EUR: "))
loan_percentage = float(input("Enter the loan percentage of the purchase price (e.g., 80 for 80%): ")) / 100
down_payment = float(input("Enter the down payment in EUR: "))
estate_agent_fee_rate = float(input("Enter the estate agent fee percentage (e.g., 3.57 for 3.57%): ")) / 100
interest_rate = float(input("Enter the interest rate (as a percentage, e.g., 4 for 4%): ")) / 100
regular_amortization_rate = float(input("Enter the regular amortization rate (e.g., 2 for 2%): ")) / 100
special_repayment = float(input("Enter the special repayment amount per year in EUR: "))
notary_fee_rate = 0.02  # 2%
purchase_tax_rate = 0.06  # 6% Berlin tax
loan_amount = purchase_price * loan_percentage
years = 10  # Initial term for recalculating the mortgage
monthly_repayment = loan_amount * (interest_rate + regular_amortization_rate) / 12

# Set start year for the calculation
start_year = 2025

# Calculating total cost and fees
estate_agent_fees = purchase_price * estate_agent_fee_rate
notary_fees = purchase_price * notary_fee_rate
purchase_tax = purchase_price * purchase_tax_rate
subtotal_fees = estate_agent_fees + notary_fees + purchase_tax
total_costs = purchase_price + subtotal_fees
remaining_purchase_price = purchase_price - down_payment
total_down_payment = down_payment + subtotal_fees

# Calculate effective interest rate
effective_interest_rate = calculate_effective_interest_rate(interest_rate, regular_amortization_rate)

# Loan Repayment Calculation
remaining_loan = loan_amount
total_interest_paid = 0
total_principal_paid = 0
yearly_data = []

# Loop to calculate loan repayment over time (finding when debt reaches zero)
debt_free_in_years = 0
while remaining_loan > 0:
    interest_payment = remaining_loan * interest_rate
    principal_payment = monthly_repayment * 12 - interest_payment
    total_payment = interest_payment + principal_payment + special_repayment
    remaining_loan -= (principal_payment + special_repayment)
    
    # If remaining loan becomes negative, set to 0
    if remaining_loan < 0:
        remaining_loan = 0

    total_interest_paid += interest_payment
    total_principal_paid += principal_payment

    debt_free_in_years += 1
    
    # Save yearly data
    yearly_data.append({
        'Year': start_year + debt_free_in_years - 1,
        'Payment': f"€{round(total_payment, 2):,.2f}",
        'Interest': round(interest_payment, 2),
        'Principal': round(principal_payment, 2),
        'Remaining debt': round(remaining_loan, 2)
    })

# Create a DataFrame for the yearly payment plan
payment_plan_df = pd.DataFrame(yearly_data)

# Mortgage Summary
mortgage_summary = {
    "Purchase price": f"€{purchase_price:,.2f}",
    "Loan percentage": f"{loan_percentage * 100:.2f}%",
    "Loan amount": f"€{loan_amount:,.2f}",
    "Down payment": f"€{down_payment:,.2f}",
    "Monthly repayment": f"€{monthly_repayment:,.2f}",
    "Interest rate": f"{interest_rate * 100:.2f}%",
    "Effective interest rate": f"{effective_interest_rate * 100:.2f}%",
    "Capital repayment": f"{regular_amortization_rate * 100:.2f}%",
    "Debt-free in": f"{debt_free_in_years} years"
}

# Display mortgage summary
print("\n--- Mortgage Calculation Summary ---")
for key, value in mortgage_summary.items():
    print(f"{key}: {value}")

# Show yearly payment plan
print("\n--- Yearly Payment Plan ---")
print(payment_plan_df)



# Purchase cost details
purchase_cost_details = {
    "Purchase price": f"€{purchase_price:,.2f}",
    "+ Estate agent fees": f"€{estate_agent_fees:,.2f}",
    "+ Notary fees": f"€{notary_fees:,.2f}",
    "+ Purchase tax": f"€{purchase_tax:,.2f}",
    "= Subtotal purchase fees": f"€{subtotal_fees:,.2f}",
    "Total costs": f"€{total_costs:,.2f}",
    "- Down payment on purchase price": f"€{down_payment:,.2f}",
    "- Purchase fees": f"€{subtotal_fees:,.2f}",
    "Loan amount": f"€{loan_amount:,.2f}",
    "Total down payment": f"€{total_down_payment:,.2f}"
}

# Show purchase cost summary
print("\n--- Purchase Cost Breakdown ---")
for key, value in purchase_cost_details.items():
    print(f"{key}: {value}")


# Plot Remaining Debt over time
plt.figure(figsize=(10, 6))
plt.plot(payment_plan_df['Year'], payment_plan_df['Remaining debt'], label='Remaining Debt', marker='o', color='red')
plt.xlabel('Year')
plt.ylabel('Remaining Debt (€)')
plt.title('Remaining Debt per Year')
plt.grid(True)
plt.show()

# Plot Interest vs Principal over time and highlight the point where interest < principal
plt.figure(figsize=(10, 6))
plt.plot(payment_plan_df['Year'], payment_plan_df['Interest'], label='Interest Payment', marker='o', color='blue')
plt.plot(payment_plan_df['Year'], payment_plan_df['Principal'], label='Principal Payment', marker='o', color='green')

# Identify the crossover year where interest < principal
crossover_year = None
for index, row in payment_plan_df.iterrows():
    if row['Interest'] < row['Principal']:
        crossover_year = row['Year']
        break

if crossover_year:
    plt.axvline(x=crossover_year, color='orange', linestyle='--', label=f'Interest < Principal (Year {crossover_year})')

# Add labels and grid
plt.xlabel('Year')
plt.ylabel('Amount (€)')
plt.title('Interest vs Principal Payments Over Time')
plt.legend()
plt.grid(True)
plt.show()
