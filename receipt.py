from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# ===== Step 1: Get Inputs =====
customer_name = input("Enter Customer Name: ")
num_items = int(input("Enter number of items: "))

items = []
for i in range(num_items):
    print(f"\nItem {i+1}:")
    item_name = input("Enter item name: ")
    qty = int(input("Enter quantity: "))
    price = float(input("Enter price per unit: "))
    total_price = qty * price
    items.append([item_name, qty, price, total_price])

discount = float(input("\nEnter discount (if any, else 0): "))

# ===== Step 2: Calculations =====
subtotal = sum([item[3] for item in items])
final_total = subtotal - discount

# ===== Step 3: Generate Invoice ID =====
invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

# ===== Step 4: Prepare Data for Table =====
DATA = [["Item", "Qty", "Price (Rs.)", "Total (Rs.)"]]

for item in items:
    DATA.append(item)

DATA.append(["Sub Total", "", "", f"{subtotal:.2f}"])
DATA.append(["Discount", "", "", f"-{discount:.2f}"])
DATA.append(["Total", "", "", f"{final_total:.2f}"])

# ===== Step 5: Create PDF =====
pdf_filename = f"bill_{invoice_id}.pdf"
pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
styles = getSampleStyleSheet()

elements = []

# --- Company Header ---
company_name = "ABC Traders Pvt. Ltd."
company_address = "123 Business Street, City Center, Mumbai, India\nPhone: +91-9876543210 | Email: info@abctraders.com"

company_title = Paragraph(f"<b>{company_name}</b>", styles["Title"])
company_addr = Paragraph(company_address, styles["Normal"])
elements.append(company_title)
elements.append(company_addr)
elements.append(Spacer(1, 20))

# --- Invoice Title ---
title_style = styles["Heading1"]
title_style.alignment = 1
title = Paragraph("Business Billing System", title_style)
elements.append(title)
elements.append(Spacer(1, 20))

# --- Customer Info + Invoice ID ---
date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
customer_info = Paragraph(
    f"<b>Invoice ID:</b> {invoice_id}<br/><b>Customer:</b> {customer_name}<br/><b>Date:</b> {date_str}",
    styles["Normal"]
)
elements.append(customer_info)
elements.append(Spacer(1, 20))

# --- Table Style ---
style = TableStyle([
    ("BOX", (0, 0), (-1, -1), 1, colors.black),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
])

table = Table(DATA, style=style)
elements.append(table)

# Build PDF
pdf.build(elements)

print(f"✅ Bill generated successfully: {pdf_filename}")
