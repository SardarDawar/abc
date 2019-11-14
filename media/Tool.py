# -*- coding: utf-8 -*-

import pandas as pd
from calendar import monthrange
import calendar 
from dateutil import relativedelta
import numpy as np
start=pd.datetime.now()

def TimeCalculatorCreditCard(AmountOwed, Payment, Rate, counter):
    interest = (AmountOwed*Rate)/12
    PrincipalPayment = Payment - interest
    Endingprincipal = AmountOwed - PrincipalPayment
    counter = counter + 1
    if Endingprincipal == 0 or Endingprincipal < 0:
        return(counter)
    else:
        return(TimeCalculatorCreditCard(Endingprincipal, Payment, Rate, counter))

def Tool(regularIncome, regularExpenses, groupobj_income, groupobj_expenses, YearlyBalances, LoanTermComparison, CashFlowSummary ):
    originalprincipal = float(inputdata.loc['Amount Owed As of Start of Tool'])
    principal = originalprincipal
    interestrate = float(inputdata.loc['Current Interest rate'])
    monthlyinstallment = float(inputdata.loc['Current Payment for Loan'])
    approvedAmountHELOC = float(inputdata.loc['APPROVED AMOUNT'])
    HELOCinterestRate = float(inputdata.loc['HELOC INITIAL INTEREST RATE'])
    CurrentDebtExpenses = float(currentDebt['Payment'].tolist()[-1])
    ProjectedHELOCInjection = float(inputdata.loc['PROJECTED INJECTION TO MORTGAGE'])
    
    def trunc_datetime(someDate):
        return someDate.replace(day=1)
        
    def Amortization(amount, flag, date):
        if flag == 0:
            return([originalprincipal, 0.0])
        
        else:
            if calendar.isleap(date.year):
                daysintheyear = float(366)
            else:
                daysintheyear = float(365)
        
            daysinthemonth = monthrange(date.year, date.month)[1]
            interestpayment = (principal*interestrate*daysinthemonth/daysintheyear)
            principalPayment =  monthlyinstallment - interestpayment
            endingPrincipal = amount - principalPayment
            return([endingPrincipal, interestpayment])
            
    def Income_Calculator(date):
        income_monthly = 0
        income_onetime = 0
        income_yearly = 0
        for group in groupobj_income:
            if group[0][0] == 'Monthly':
                parameter = trunc_datetime(group[1]['Income Starts '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['Income Ends '].tolist()[0].date())
                if(parameter == True):
                    income_monthly = income_monthly + float(group[1]['Amount'].tolist()[0])
                
            if group[0][0] == 'One Time':                
                parameter = ((trunc_datetime(group[1]['Income Starts '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['Income Ends '].tolist()[0].date()))
                                & (date.month == group[1]['Income Starts '].tolist()[0].month))
                if(parameter == True):
                    income_onetime = income_onetime + float(group[1]['Amount'].tolist()[0])               
        
            if group[0][0] == 'Yearly':
                parameter = ((trunc_datetime(group[1]['Income Starts '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['Income Ends '].tolist()[0].date()))
                                & (date.month == group[1]['Income Starts '].tolist()[0].month))
                if(parameter == True):
                    income_yearly = income_yearly + float(group[1]['Amount'].tolist()[0])
                
    
        TotalIncome = income_monthly + income_yearly + income_onetime
        return(TotalIncome)
        
        
    def Expense_Calculator(date):
        expense_monthly = 0
        expense_onetime = 0
        expense_yearly = 0
        for group in groupobj_expenses:
            if group[0][0] == 'Monthly':
                parameter = trunc_datetime(group[1]['Start Date '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['End Date '].tolist()[0].date())
                if(parameter == True):
                    expense_monthly = expense_monthly + float(sum(group[1]['Amount'].tolist()))
                
            if group[0][0] == 'One Time':                
                parameter = ((trunc_datetime(group[1]['Start Date '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['End Date '].tolist()[0].date()))
                                & (date.month == group[1]['Start Date '].tolist()[0].month))
                if(parameter == True):
                    expense_onetime = expense_onetime + float(sum(group[1]['Amount'].tolist()))               
        
            if group[0][0] == 'Yearly':
                parameter = ((trunc_datetime(group[1]['Start Date '].tolist()[0].date()) <= trunc_datetime(date.date()) <= trunc_datetime(group[1]['End Date '].tolist()[0].date()))
                                & (date.month == group[1]['Start Date '].tolist()[0].month))
                if(parameter == True):
                    expense_yearly = expense_yearly + float(sum(group[1]['Amount'].tolist()))
                
    
        TotalExpense = expense_monthly + expense_yearly + expense_onetime
        return(TotalExpense)
    
      
    def Debt_Calculator(date):
        sumDebt = 0
        for item in currentDebt.index:
            parameter = trunc_datetime(currentDebt.loc[item, 'As of'].date()) <= trunc_datetime(date.date()) <= trunc_datetime(currentDebt.loc[item, 'Paid off'].date())
            if parameter == True:
                sumDebt = sumDebt + currentDebt.loc[item, 'Payment']
            
        return(sumDebt)
    
    def HELOCInterestCalculator(Amount, date):
        if calendar.isleap(date.year):
            daysintheyear = float(366)
        else:
            daysintheyear = float(365)
        
        daysinthemonth = monthrange(date.year, date.month)[1]
    
        interest = (HELOCinterestRate/daysintheyear)*Amount*daysinthemonth
        return(interest)
        
    def LumpSumIncomeCalculator(date):
        LumpSumIncome = 0
        if LumpSumIncomedf.index.size == 0:
            return(LumpSumIncome)
        
        else:
            for item in LumpSumIncomedf.index:
                parameter = trunc_datetime(LumpSumIncomedf.loc[item, 'When Injecting'].date()) == trunc_datetime(date.date())
                if parameter == True:
                    LumpSumIncome = LumpSumIncome + LumpSumIncomedf.loc[item, 'Amount']
            
            return(LumpSumIncome)
    
    def LumpSumExpensesCalculator(date):
        LumpSumExpenses = 0
    
        if LumpSumExpensesdf.index.size == 0:
            return(LumpSumExpenses)
        
        else:
            for item in LumpSumExpensesdf.index:
                parameter = trunc_datetime(LumpSumExpensesdf.loc[item, 'When Expended'].date()) == trunc_datetime(date.date())
                if parameter == True:
                    LumpSumExpenses = LumpSumExpenses + LumpSumExpensesdf.loc[item, 'Amount']
            
            return(LumpSumExpenses)
    
    startpoint = pd.datetime.now()
    Loanperiod = int(inputdata.loc['Terms of Rate'])
    endpoint = startpoint + pd.DateOffset(years = Loanperiod) 
    endpoint = endpoint + pd.DateOffset(months = 1)
    
    daterange = pd.date_range(start = startpoint.date(), end = endpoint.date(), freq ='M')
    count = 0
    prevColumnname = daterange[0].strftime('%b-%y')
    interestPrimaryLoan = 0
    interestPrimaryLoanuisngTool = 0
    HELOCInterestSum = 0
    prevstuff = daterange[0]
    
    for stuff in daterange:
        columnname = stuff.strftime('%b-%y')
        CashFlowSummary[columnname] = None
    
        updatedamount = round(Amortization(principal, count,  prevstuff)[0],2)
        interestPrimaryLoan = interestPrimaryLoan + round(Amortization(principal, count,  prevstuff)[1],2)
        principal = updatedamount
        if updatedamount < 0:
            updatedamount = 0
            
        CashFlowSummary.loc['Original P&I Loan Balance', columnname] = updatedamount
        
        if stuff.month == 2:
            YearlyBalances = YearlyBalances.append({'Date': 'January-' + str(stuff.year), 'Original P&I Loan' : CashFlowSummary.loc['Original P&I Loan Balance', prevColumnname], 'HELOC': CashFlowSummary.loc['HELOC Opening Balance', prevColumnname], 'P&I with Injections': CashFlowSummary.loc['New P&I Loan Balance with Injections', prevColumnname]}, ignore_index=True)
       
        if (updatedamount == 0) or (stuff == daterange[-1]):
            endDatePrimaryLoan = stuff
            break
        
        if count > 3 and CashFlowSummary.loc['New P&I Loan Balance with Injections', prevColumnname] == 0:
            prevstuff = stuff
            prevColumnname = columnname
            count = count + 1
            CashFlowSummary.loc['New P&I Loan Balance with Injections', columnname] = 0
            CashFlowSummary.loc['HELOC Opening Balance', columnname] = 0
            continue
        
        CashFlowSummary.loc['Original HELOC Credit Limit', columnname] = approvedAmountHELOC
        CashFlowSummary.loc['HELOC Interest Rate', columnname] = HELOCinterestRate
    
        Income = Income_Calculator(stuff)
        CashFlowSummary.loc['Regular Income', columnname] = Income
        LumpsumIncome = float(LumpSumIncomeCalculator(stuff))
        CashFlowSummary.loc['Lump Sum Income', columnname] = LumpsumIncome
        TotalIncome = round((Income + LumpsumIncome),2)
        CashFlowSummary.loc['TOTAL INCOME', columnname] = TotalIncome
    
        Expense = Expense_Calculator(stuff)
        CashFlowSummary.loc['Regular Expenses', columnname] = Expense
        LumpsumExpenses = float(LumpSumExpensesCalculator(stuff))
        CashFlowSummary.loc['Lump Sum Expenses', columnname] = LumpsumExpenses
        CurrentDebtExpenses = Debt_Calculator(stuff)
        CashFlowSummary.loc['Current Debt Expenses', columnname] = CurrentDebtExpenses
        CashFlowSummary.loc['P&I Loan Payment Expense', columnname] = monthlyinstallment
        TotalExpense = round((Expense + LumpsumExpenses + CurrentDebtExpenses + monthlyinstallment), 2)
        CashFlowSummary.loc['TOTAL EXPENSES', columnname] = TotalExpense
        CashFlowSummary.loc['PROJECTED INJECTION TO MORTGAGE', columnname] = 0
    
        if count == 0:
            HELOCOpeningBalance = ProjectedHELOCInjection
            PILoanBalancewithInjections = round((updatedamount-ProjectedHELOCInjection),2)
            CashFlowSummary.loc['PROJECTED INJECTION TO MORTGAGE', columnname] = HELOCOpeningBalance
          
        if count != 0:
            HELOCOpeningBalance = CashFlowSummary.loc['HELOC Closing Balance (Forecasted)', prevColumnname]
            if count == 1:
                principalforPILoanBalance = CashFlowSummary.loc['New P&I Loan Balance with Injections', prevColumnname]
            if count != 1:
                principalforPILoanBalance = CashFlowSummary.loc['New P&I Loan Balance with Injections', prevColumnname] - CashFlowSummary.loc['PROJECTED INJECTION TO MORTGAGE', prevColumnname]
            
            PILoanBalancewithInjections = round(Amortization(principalforPILoanBalance, count, stuff)[0],2) 
            interestPrimaryLoanuisngTool = interestPrimaryLoanuisngTool + round(Amortization(principalforPILoanBalance, count, stuff)[1],2)
            if HELOCOpeningBalance <= 3000:
                prevsurplus = CashFlowSummary.loc['Surplus from checking (injected into P&I)', prevColumnname]
                CashFlowSummary.loc['PROJECTED INJECTION TO MORTGAGE', columnname] = float((ProjectedHELOCInjection + HELOCOpeningBalance + prevsurplus))
                HELOCOpeningBalance = ProjectedHELOCInjection
                
        CashFlowSummary.loc['HELOC Opening Balance', columnname] = HELOCOpeningBalance
    
        if PILoanBalancewithInjections < 0:
            PILoanBalancewithInjections = 0

        surplus = TotalIncome - TotalExpense - HELOCOpeningBalance
        if surplus < 0:
            surplus = 0
    
        HELOCInteresttobeCalculatedon = HELOCOpeningBalance + TotalExpense - TotalIncome
        if surplus > 0:
            HELOCInterest = 0
        else:
            HELOCInterest = HELOCInterestCalculator(HELOCInteresttobeCalculatedon, stuff )
        CashFlowSummary.loc['HELOC Interest Paid', columnname] = round(HELOCInterest,2)
    
        HELOCInterestSum = HELOCInterestSum + round(HELOCInterest,2)
     
        HELOCReducedBy = TotalIncome - TotalExpense - round(HELOCInterest,2)-surplus
        CashFlowSummary.loc['HELOC Reduced by', columnname] = HELOCReducedBy
    
        CashFlowSummary.loc['HELOC Closing Balance (Forecasted)', columnname] = HELOCOpeningBalance - HELOCReducedBy

        CashFlowSummary.loc['New P&I Loan Balance with Injections', columnname] = PILoanBalancewithInjections
  
        CashFlowSummary.loc['HELOC Buffer Available', columnname] = approvedAmountHELOC - HELOCOpeningBalance
    
        CashFlowSummary.loc['Surplus from checking (injected into P&I)', columnname] = surplus
            
        if CashFlowSummary.loc['New P&I Loan Balance with Injections', columnname] == 0:
            endDatePrimaryLoanusingTool = stuff
    
        prevstuff = stuff
        prevColumnname = columnname
        count = count + 1
       
    MonthsforPrimaryLoan = relativedelta.relativedelta(endDatePrimaryLoan, startpoint.replace(day = 1))
    MonthsforPrimaryLoanusingTool = relativedelta.relativedelta(endDatePrimaryLoanusingTool, startpoint)

    HELOCPayoffMonth = endDatePrimaryLoanusingTool.strftime('%B')
    HELOCPayoffYear = endDatePrimaryLoanusingTool.strftime('%Y')

    LoanTermComparison = LoanTermComparison.append({'Loan Type': 'Primary Loan',   'Value': originalprincipal, 'Years': MonthsforPrimaryLoan.years, 'Months': MonthsforPrimaryLoan.months, 'Interest Cost': interestPrimaryLoan }, ignore_index=True)
    LoanTermComparison = LoanTermComparison.append({'Loan Type': 'Primary Loan Using Tool',   'Value': originalprincipal, 'Years': MonthsforPrimaryLoanusingTool.years, 'Months': MonthsforPrimaryLoanusingTool.months, 'Interest Cost': interestPrimaryLoanuisngTool }, ignore_index=True)
    LoanTermComparison = LoanTermComparison.append({'Loan Type': 'HELOC Payoff -> month+year', 'Years': HELOCPayoffYear, 'Months': HELOCPayoffMonth, 'Interest Cost': HELOCInterestSum }, ignore_index=True)
    return([CashFlowSummary, YearlyBalances, LoanTermComparison])
            
#DataLoading
path = "G:\AIP website work\Data"

inputdata = pd.read_csv(path + '\\InputData1.csv')
inputdata.set_index('INPUTS', inplace=True)

currentDebt = pd.read_csv(path + '\\CurrentDebt.csv')
currentDebt['As of'] = pd.to_datetime(currentDebt['As of'], format='%d-%m-%y', errors='coerce')

for item in currentDebt.index:
    counter = 0
    if currentDebt.loc[item, 'Rate'] < 0.0001:
        monthsinpaying = (currentDebt.loc[item, 'Owed'])/float(currentDebt.loc[item, 'Payment'])
        monthsinpaying = int(np.ceil(monthsinpaying))
        PaidoffDate = currentDebt.loc[item, 'As of'] + pd.DateOffset(months = monthsinpaying)
        currentDebt.loc[item, 'Paid off'] = PaidoffDate
        
    else:
        monthsinpaying = TimeCalculatorCreditCard(currentDebt.loc[item, 'Owed'], currentDebt.loc[item, 'Payment'], currentDebt.loc[item, 'Rate'], counter)
        PaidoffDate = currentDebt.loc[item, 'As of'] + pd.DateOffset(months = monthsinpaying)
        currentDebt.loc[item, 'Paid off'] = PaidoffDate
        

regularExpenses = pd.read_csv(path + '\\RegularExpensedData.csv')
regularExpenses['Start Date '] = pd.to_datetime(regularExpenses['Start Date '], format='%d-%m-%y', errors='coerce')
regularExpenses['End Date '] = pd.to_datetime(regularExpenses['End Date '], format='%d-%m-%y', errors='coerce')
regularExpenses['Amount'] = regularExpenses['Amount'].fillna(0)

regularIncome = pd.read_csv(path + '\\RegularIncomeData.csv')
regularIncome['Income Starts '] = pd.to_datetime(regularIncome['Income Starts '], format='%d-%m-%y', errors='coerce')
regularIncome['Income Ends '] = pd.to_datetime(regularIncome['Income Ends '], format='%d-%m-%y', errors='coerce')
regularIncome['Amount'] = regularIncome['Amount'].fillna(0)


LumpSumIncomedf = pd.read_csv(path + '\\LumpSumIncome.csv')
LumpSumIncomedf['When Injecting'] = pd.to_datetime(LumpSumIncomedf['When Injecting'], format='%d-%m-%y', errors='coerce')
LumpSumIncomedf['Amount'] = LumpSumIncomedf['Amount'].fillna(0)

LumpSumExpensesdf = pd.read_csv(path + '\\LumpSumExpenses.csv')
LumpSumExpensesdf['When Expended'] = pd.to_datetime(LumpSumExpensesdf['When Expended'], format='%d-%m-%y', errors='coerce')
LumpSumExpensesdf['Amount'] = LumpSumExpensesdf['Amount'].fillna(0)

groupobj_income = regularIncome.groupby(['Frequency', 'Description', 'Income Starts ']) 
groupobj_expenses = regularExpenses.groupby(['Frequency', 'Description', 'Start Date ']) 

#OuputDataFormat
CashFlowSummary = pd.read_csv(path + '\\OutputFormat.csv')
CashFlowSummary.set_index('P&I & HELOC Details', inplace=True)
YearlyBalances = pd.DataFrame(columns=['Date', 'Original P&I Loan', 'HELOC', 'P&I with Injections'])
LoanTermComparison = pd.DataFrame(columns=['Loan Type', 'Value', 'Years', 'Months', 'Interest Cost'])

Output = Tool(regularIncome, regularExpenses, groupobj_income, groupobj_expenses, YearlyBalances, LoanTermComparison, CashFlowSummary)

#outputs
Output[0].fillna(0, inplace=True)
Output[1].fillna(0, inplace=True)

#Outputfilewriting
path = path + '\\Outputs'
writer_CashFlowSummary = pd.ExcelWriter(path + '\\CashFlowSummary.xlsx', engine='xlsxwriter')
writer_YearlyBalances = pd.ExcelWriter(path + '\\YearlyBalances.xlsx', engine='xlsxwriter')
writer_LoanTermComparison = pd.ExcelWriter(path + '\\LoanTermComparison.xlsx', engine='xlsxwriter')

Output[0].to_excel(writer_CashFlowSummary, sheet_name='Sheet1')
Output[1].to_excel(writer_YearlyBalances, sheet_name='Sheet1')
Output[2].to_excel(writer_LoanTermComparison, sheet_name='Sheet1')

print("Do you want to see what happens if your income/expenses increased or decreased?")
signal_income = input("Enter Yes/No for change in income: ")
signal_expenses =  input("Enter Yes/No for change in expenses: ")

if signal_income == ("yes" or "Yes"):    
    Amount = input("Enter by how much the income has increase/decreased (use -ve sign for decrement) : ")
    Frequency = input("Enter frequency of the income (Type one among these -> [Yearly, Monthly, One Time) : ")
    IncomeStarts = input("Enter date when the income has started accruing (dd-mm-yy, e.g. 01-07-19): ")
    IncomeEnds = input("Enter date when the income has stopped accruing (dd-mm-yy, e.g. 01-10-38): ")
    

    IncomeStarts = pd.to_datetime(IncomeStarts, format='%d-%m-%y', errors='coerce')
    IncomeEnds = pd.to_datetime(IncomeEnds, format='%d-%m-%y', errors='coerce')
    regularIncome = regularIncome.append({'Description': "Income", 'Type': "Salary", 'Amount': float(Amount), 'Frequency': Frequency, 'Income Starts ': IncomeStarts, 'Income Ends ': IncomeEnds}, ignore_index=True)

    groupobj_income = regularIncome.groupby(['Frequency', 'Description', 'Income Starts '])

    
if signal_expenses == ("yes" or "Yes"):
    Amount = raw_input("Enter by how much the expense has increase/decreased (use -ve sign for decrement) : ")
    Frequency = raw_input("Enter frequency of the expense (Type one among these -> [Yearly, Monthly, One Time) : ")
    StartDate = raw_input("Enter date when the expense has started accruing (dd-mm-yy, e.g. 01-07-19): ")
    EndDate = raw_input("Enter date when the expense has stopped accruing (dd-mm-yy, e.g. 01-10-38): ")
    

    StartDate = pd.to_datetime(IncomeStarts, format='%d-%m-%y', errors='coerce')
    EndDate = pd.to_datetime(IncomeEnds, format='%d-%m-%y', errors='coerce')
    regularExpenses = regularExpenses.append({'Description': "Miscellaneous", 'Type': "Something", 'Amount': float(Amount), 'Frequency': Frequency, 'Start Date ': StartDate, 'End Date ': EndDate}, ignore_index=True)

    groupobj_expenses = regularExpenses.groupby(['Frequency', 'Description', 'Start Date ']) 
    
    
if signal_income == ("yes" or "Yes") or signal_expenses == ("yes" or "Yes"):

    Output1 = Tool(regularIncome, regularExpenses, groupobj_income, groupobj_expenses, YearlyBalances, LoanTermComparison, CashFlowSummary)
    #outputs
    Output1[0].fillna(0, inplace=True)
    Output1[1].fillna(0, inplace=True)

    Output1[0].to_excel(writer_CashFlowSummary, sheet_name = 'Sheet2')
    Output1[1].to_excel(writer_YearlyBalances, sheet_name = 'Sheet2')
    Output1[2].to_excel(writer_LoanTermComparison, sheet_name = 'Sheet2')

else:
    pass

writer_CashFlowSummary.save()
writer_YearlyBalances.save()
writer_LoanTermComparison.save()


print(pd.datetime.now()-start)
    
        
    

    
    


        
