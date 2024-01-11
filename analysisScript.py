import pandas as pd
from prettytable import PrettyTable

# First of all, we need to read the file px_etf and create a dataframe to transform the data.
ETFprices = pd.read_csv('px_etf.csv')

# Transform the first column to date data type, so we can extract days, month, etc...
ETFprices['date'] = pd.to_datetime(ETFprices['date'])

# Reproduce same steps with the tx_etf.csv file.
ETFtransactions = pd.read_csv('tx_etf.csv')

ETFtransactions['date'] = pd.to_datetime(ETFtransactions['date'])

#Create two column for both dataframes. This columns will help creating the final solution, distinguishing between the transactions in new months and/or years 
ETFprices['year'] = ETFprices['date'].dt.year
ETFprices['month'] = ETFprices['date'].dt.month

ETFtransactions['year'] = ETFtransactions['date'].dt.year
ETFtransactions['month'] = ETFtransactions['date'].dt.month

""" 
    This function will add to the list "listOfPositions" the position of the portfolio, the amount of ETFs it has after any transaction.
    @param ETFname: The name of the ETF of the last transaction
    @param ETFqty: The number of ETFs that have been in that transaction
    @param operation: describes the type of operation, SELL or BUY

"""
tablePortfolio = PrettyTable()
tablePortfolio.field_names =  ["Year", "End of the Year ETFs in Portfolio", "Total Amount"]
portfolioLastOperation = {}

def transactionPortfolioPosition(ETFname, ETFqty, operation):
    
    if ETFname in portfolioLastOperation and operation == 'BUY':
        portfolioLastOperation[ETFname] += ETFqty
    elif ETFname in portfolioLastOperation:
        portfolioLastOperation[ETFname] -= ETFqty
    else:
        portfolioLastOperation.update({ETFname: ETFqty})

"""
This function will save into the table "tablePortfolio" the ETFs and the total amount of ETFs that the portfolio have at the year of any Year.
@param year
@param dict
"""
def savePortfolioPositions(year, dict):

    etfNameQty = ""
    totalQty = 0
    for etf, quantity in dict.items():
        totalQty += quantity
        etfNameQty += f"{etf}: " + f"{quantity} / "

    tablePortfolio.add_row([year, etfNameQty, totalQty])

    tablePortfolio.align["ETFs in Portfolio"] = "l"  # Left-align the stock column    

# Create variables that will store the total revenue every transaction creates
totalAmount = 0

# Two variables to set the year and month of the first transaction
year, month = ETFtransactions.at[0, 'year'], ETFtransactions.at[0, 'month']

# This variable will create the table where the solution will be set.
tableRevenue = PrettyTable()
tableRevenue.field_names = ["Year", "Month", "Portfolio Performance (USD)", "Perfomance %"]

# This variables will trace the total amount of the portfolio for the end of a month or year and the last one will identify the last transaction.
previous_year_amount = 0
previous_month_amount = 0
lastRowIndex = len(ETFtransactions) - 1

# Last but not least, to create the charts I will need a data source 
monthColumns = ['Year', 'Month', 'Month Revenue', 'Month Performance', 'Total Amount']
monthDataGraphic = []

yearColumns = ['Year', 'Year Revenue', 'Year Performance', 'Total Amount']
yearDataGraphic = []

"""
 This for loop will iterate through every transaction in the Dataframe. For every transaction, the first thing it will do is to see if it is check if there is a new month or the transaction is the 
 last one and for every operation it will add or rest a certain amount tot the script's variable totalAmount, who consists in the amount in USD of the portfolio assets. Apart from that, in this
 for loop, there will be new lines added to the final table solution every time there is a new month or new year.
"""

for transaction in ETFtransactions.itertuples():
    
    # Define the year and month of the current transaction
    currentyear, currentmonth = transaction[5], transaction[6]
    
    #Check the prices of the ETF for the given date
    rowPrice = ETFprices[ETFprices['date'] == transaction.date]    
    
    # Get the quantity of the transaction
    transactionQTY = transaction.qty

    #Call function to save the status of the portfolio.
    transactionPortfolioPosition(transaction.ticker, transactionQTY, transaction.order)
    
    #Update the total amount in USD of the portfolio and to avoid not adding the last row
    if transaction.order == 'SELL' and transaction.Index == lastRowIndex:
        totalAmount += rowPrice[transaction.ticker].iloc[0] * transactionQTY
    elif transaction.Index == lastRowIndex: 
        totalAmount -= rowPrice[transaction.ticker].iloc[0] * transactionQTY
        
    #If the transaction is from a different month or is the last one, we will actualize the variables and insert one row.
    if month != currentmonth or transaction.Index == lastRowIndex:
        
        # Calculate the revenue for the monht that just has ended
        monthRevenue = totalAmount - previous_month_amount
        
        #To handle negative values regarding the revenue and the initial month operations, the script will multiply it by -100 and not by 100, as the 
        if previous_month_amount > 0:
            monthPercentage = (monthRevenue/previous_month_amount) * 100
        elif previous_month_amount < 0:
            monthPercentage = (monthRevenue/previous_month_amount) * -100
        else:
            monthPercentage = 0
        
        # Insert into the solution table the information regarding the portfolio monthly performance.
        tableRevenue.add_row([year, month, f" Month Revenue (USD): {monthRevenue:.2f} ", f"Month Performance: {monthPercentage:.2f}%"])
        
        # Insert a row in the list "yearDataGraphic" to generate a dataframe that will contain necessary data for generating charts
        monthDataGraphic += [[year,  month , monthRevenue, monthPercentage, totalAmount]]

        #Knowing that the month has changed, let check for the year too and also if is the last transaction.
        if year != currentyear or transaction.Index == lastRowIndex:
            
            # Calculate the revenue for the year that just ended
            yearRevenue = totalAmount - previous_year_amount

            # Same as in the case of the previous month amount
            if previous_year_amount > 0:
                yearPercetange = (yearRevenue/previous_year_amount) * 100
            elif previous_year_amount < 0:
                yearPercetange = (yearRevenue/previous_year_amount) * -100
            else:
                yearPercetange = 0

            #The first year does not have any other year to compare, so to avoid putting missinformation regarding the revenue, the script will put none for the first year
            if previous_year_amount == 0:
                tableRevenue.add_row([year, '', f" Total amount {totalAmount:.2f}", f"Year Performance {yearPercetange:.2f}%"])
            else:
                tableRevenue.add_row([year, '', f" Year revenue (USD): {yearRevenue:.2f} and total amount {totalAmount:.2f}", f"Year Performance {yearPercetange:.2f}%"])
            
            # Insert a row in the list "yearDataGraphic" to generate a dataframe that will contain necessary data for generating charts
            yearDataGraphic += [[year, yearRevenue, yearPercetange, totalAmount]]

            #Add a decoration row to separate new years. Apart from that, for the yearly portfolio position of the ETFs, the script will call the function "savePortfolioPositions"
            tableRevenue.add_row(['----', '----', '-----------', '----'])
            savePortfolioPositions(year, portfolioLastOperation)
            
            # Update the variables regarding the existence of a new year
            previous_year_amount = totalAmount
            year = currentyear
        
        #Update the variables regarding the existence of a new month.
        previous_month_amount = totalAmount
        month = currentmonth

    # If there is no new month or it is not yet the last transaction, the loop will just update the variable totalAmount.
    if transaction.order == 'SELL':
            totalAmount += rowPrice[transaction.ticker].iloc[0] * transactionQTY
    else: 
        totalAmount -= rowPrice[transaction.ticker].iloc[0] * transactionQTY


# Finally, the solution is the table printed below:
print(tableRevenue)
print()
print(tablePortfolio)


# Generates the dataframes to create the csv files that will be used to create charts
monthGraphic = pd.DataFrame(monthDataGraphic, columns = monthColumns)
monthGraphic.to_csv('monthlyData.csv', index = False)

yearGraphic = pd.DataFrame(yearDataGraphic, columns = yearColumns)
yearGraphic.to_csv('yearlyData.csv', index = False)