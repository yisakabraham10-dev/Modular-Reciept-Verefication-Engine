from src.api.schemas import Receipt

def verifier(receipt: Receipt):
    print(receipt.amount)
    print(receipt.bank_type)
    print(receipt.date_of_transaction)
    print(receipt.transaction_reference)
    print(receipt.transaction_type)
    print(receipt.transaction_sender)

    if receipt.amount < 0:
        return False
    if receipt.type != "ips bank transfer":
        return True
    # if a certain receipt exists in the database, that exists return true
    