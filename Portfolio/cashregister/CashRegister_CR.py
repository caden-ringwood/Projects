#Caden Ringwood
#Cash Reister
#9/24/2021

numItems = 4
costPerItem = 10.00
subTotal = numItems * costPerItem
taxRate = 0.08
taxAmount = subTotal * taxRate
totalPrice = taxAmount + subTotal

print("SALES RECEIPT")
print("Number of items         :  "+str(numItems))
print("Cost per item              : $"+str(costPerItem))
print("Tax rate                       : "+str(taxRate))
print("Tax amount                 : $"+str(taxAmount))
print("TOTAL SALE PRICE: $"+str(totalPrice))

