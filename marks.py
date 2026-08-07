medicines = ["paracetamol", "metformin", "amlodipine", "salbutamol"]

expiry_date = ["1-1-2026", "2-3-2026", "4-5-2026", "3-5-2026"]

quantity = [10, 9, 45, 30]

# Display medicine details
for i in range(len(medicines)):
    print(f"Medicine: {medicines[i]} | Expiry Date: {expiry_date[i]} | Quantity: {quantity[i]}")

# Check for low stock
for i in range(len(quantity)):
    if quantity[i] < 20:
        print(f"Medicine: {medicines[i]} is running low. Please restock.")