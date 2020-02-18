
import random
import math
import numpy.random as np
import matplotlib.pyplot as plt
import time

class Business:
    def __init__(self):
        self.MonthlySales = []
        self.IdealPrice = 10
        self.Demand = 0.5
        self.BankAccount = 100
        self.DesiredBankAccount = 0
        self.StockProductionCost = 5
        self.Price = 1.8*self.StockProductionCost
        self.MonthlyStockProduction = 20
        self.Month = 0
        self.UpkeepPerStockCapacity = 1
        self.EndMonth = 1200
        self.Stock = 0
        self.StockCapacity = 50
        self.BankAccountList = []

    def Probability(self, Demand):
        """
        Calculates using the demand whether a consumer buys the product,
        This uses demand as a probability and returns a boolean value
        as to whether the product is bought or not
        """
        RandomValue = random.randint(0, 100)
        if (RandomValue/100) < Demand:
            return True
        else:
            return False

    def RandomProbability(self):
        RandomProbability = np.normal(0, 0.3, 1)
        Probability = RandomProbability*0.3
        return Probability

    def ProduceStock(self, BankAccount, Cost, MonthlyProduction, StockSpace):
        ProducedStock = 0
        while (ProducedStock < MonthlyProduction) and BankAccount > 0 and StockSpace != 0:
            BankAccount -= Cost
            ProducedStock += 1
            StockSpace -= 1
        return ProducedStock, BankAccount

    def PrintStats(self, BankAccount, Stock, Price, Demand, Capacity):
        """
        Outputs all the statistics about the current month
        """
        print("Bank Account: "+str(BankAccount))
        print("Stock: "+str(Stock))
        print("Price: "+str(Price))
        print("Demand: "+str(Demand))
        print("Capacity: "+str(Capacity))
        print("-"*10)

    def CalculateDemand(self, Price, Cost):
        """
        Calculates a value for demand, needs to be between 1 and 0, currently
        works using an inverse dependancy to profit
        Needs work
        """
        Demand = 1/(Price/Cost)
        Demand += self.RandomProbability()
        return Demand

    def ConsumerBuyingStock(self, Stock, Price, Demand):
        """
        Returns the amount of sold stock and revenue gained per month
        works out whether the stock has sold based off of the demand probability
        """
        SoldStock, Revenue = 0, 0
        for Unit in range(0, Stock):
            BoughtUnit = self.Probability(Demand)
            if BoughtUnit == True:
                SoldStock += 1
                Revenue += Price
        return SoldStock, Revenue

    def InvestMoney(self, BankAccount, MonthlyStockProduction, StockCapacity):
        """
        Function that could run once the bank account has reached a certain point
        Uses some of the money and increases the stock capactity and stock production
        """
        InvestRate = (math.floor(BankAccount/1000))
        MonthlyStockProduction += MonthlyStockProduction*0.1*InvestRate
        StockCapacity += 10
        SpentMoney = InvestRate*1000
        return SpentMoney, MonthlyStockProduction, StockCapacity

    def MonthlyFixedCostCalculation(self, Capacity):
        """
        The fixed costs of the business, currently only based on the
        stock capactity of the business
        """
        Costs = 0
        Costs += Capacity * 1
        return Costs

    def main(self):
        while self.Month != self.EndMonth:
            self.PrintStats(self.BankAccount, self.Stock, self.Price, self.Demand, self.StockCapacity)
            if self.Stock < self.StockCapacity:
                if self.Stock == 0 and self.BankAccount < self.StockProductionCost:
                    #print("Ran out of money")
                    return self.BankAccountList, self.Month, self.MonthlySales
            else:
                self.Price -= 1
            if self.BankAccount < self.DesiredBankAccount:
                self.Price += 1

            ProducedStock, self.BankAccount = self.ProduceStock(self.BankAccount, self.StockProductionCost, self.MonthlyStockProduction, self.StockCapacity-self.Stock)
            self.Stock += ProducedStock
            self.MonthlySales.append(ProducedStock)
            self.Demand = self.CalculateDemand(self.Price, self.StockProductionCost)
            SoldStock, Revenue = self.ConsumerBuyingStock(self.Stock, self.Price, self.Demand)
            self.Stock -= SoldStock
            self.BankAccount += Revenue
            self.BankAccount -= self.MonthlyFixedCostCalculation(self.StockCapacity)

            if self.BankAccount > 4500:
                SpentMoney, self.MonthlyStockProduction, self.StockCapacity = self.InvestMoney(self.BankAccount, self.MonthlyStockProduction, self.StockCapacity)
                self.BankAccount -= SpentMoney
            self.Month += 1
            self.BankAccountList.append(self.BankAccount)

        return self.BankAccountList, self.Month, self.MonthlySales

def CreateGraph(XList1, XList2, YList):
    XLabel = "Month"
    YLabel = "Bank Balance"
    '''plt.plot(XList, YList)
    plt.xlabel(XLabel)
    plt.ylabel(YLabel)
    plt.show()'''
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel(XLabel)
    ax1.set_ylabel(YLabel, color=color)
    ax1.plot(YList, XList1, color=color)

    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel("Monthly Sales", color=color)  # we already handled the x-label with ax1
    ax2.plot(YList, XList2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    axes = plt.gca()


    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

Months = []
business = Business()
MoneyList, FinalMonth, MonthlySales = business.main()
for i in range(FinalMonth):
    Months.append(i)

CreateGraph(MoneyList, MonthlySales, Months)