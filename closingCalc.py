#closingCalc.py
#Tuff's Totts 
#Eric, Moses, Saad, Thomas
#Objective of this program is to output total payment, expense, deposut and difference given current day sales 
#The many functions used in this project range to simple addition, printing to currency division 
#2-14-2025


#Function to distrubute tips (Convert credit tip to cash tip by taking out appropiate amount of paper currency)
def disTips(exp, p100, p50, p20, p10, p5, p1):
    
    return 

#Function to calculate paper currency (100s, 50s, 20s, 10s, 5s, 2s and 1s)
def calcPaper(p100, p50, p20, p10, p5, p2, p1):
    paper = p100+p50+p20+p10+p5+p1
    print(f"Paper Currency: ${paper}")
    return paper 

#Function to calculate coin currency (coin dollars, 50 cent coins, quarters, dimes, nickles and pennies)
def calcCoin(c100, c50, c25, c10, c5, c1):
    coin = c100+c50+c25+c10+c5+c1
    print(f"Coin Currency:${coin}")
    return coin 

#Function to calculate total cash, addition of coins and paper currency 
def calcCash(coin, paper):
    csh = coin + paper
    print(f"Cash: ${csh}")
    return csh

#Function to calculate total (last night balance + total Payment of current day)
def calcTotal(lastNightBalance, totalP):
    total = lastNightBalance + totalP
    print(f"Total: {total}")
    return total

#Function to calculate sum (additon of expense, credit and cash )
def calcSum(exp, crd, csh):
    sum = exp + crd + csh
    print(f"Sum: {sum}")
    return sum 

#Function to calculate deposit (sum of the larger bills 100s, 50s and 20s)
def calcDep(p100, p50, p20):
    dep = p100 + p50 + p20
    print(f"Deposit: {dep}")
    return dep

#Function to calculate leftover money for tomorrow morning
def calcLeftOver(csh, dep):
    leftOver = csh - dep
    print(f"Left over cash for tomorrow: {leftOver}")
    return leftOver 

#Function to difference
def calcDiff(sum, total):
    diff = sum - total
    print(f"Difference: {diff}")
    return diff

#main
print("Welcome to Closing Calculator created by Tuffy's Totts")

#Ideally we find a way to automate the process of counting, maybe a seperate code using an arudino to comminicate with this program  
user_input = input("Enter currency separated by spaces: 100s, 50s, 20s, 10s, 5s, 2s, 1s")
paperCurrency = list(map(int, user_input.split()))

user_input = input("Enter coins separated by spaces: dollar coin, 50 cent coin, quarter, dime, nickel, penny")
coinCurrency = list(map(int, user_input.split()))

user_input = input("Enter last night's balance: ")
lastNightsBalance = user_input

user_input = input("Enter total payment: ")
totalP = user_input

total = calcTotal(lastNightsBalance, totalP)

user_input = input("Enter tips: ")
tips = user_input
exp = tips *.9

user_input = input("Enter credit: ")
crd = user_input


csh = calcCash(paperCurrency, coinCurrency)

sum = calcSum(exp, crd, csh)

diff = calcDiff(sum, total)

dep = calcDep(calcPaper(0), calcPaper(1), calcPaper(2))

leftOver = calcLeftOver(csh, dep)

