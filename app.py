from flask import Flask, render_template, request, jsonify, send_file
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    try:
        data = request.get_json()
        
        # Extract data from request
        customer_name = data.get('customer_name', '')
        company_info = data.get('company_info', {})
        items = data.get('items', [])
        discount = float(data.get('discount', 0))
        tax = float(data.get('tax', 0))
        
        # Calculations
        subtotal = sum([item['quantity'] * item['price'] for item in items])
        tax_amount = subtotal * (tax / 100)
        final_total = subtotal - discount + tax_amount
        
        # Generate Invoice ID
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Prepare Data for Table
        DATA = [["Item", "Qty", "Price (Rs.)", "Total (Rs.)"]]
        
        for item in items:
            total_price = item['quantity'] * item['price']
            DATA.append([item['name'], item['quantity'], f"{item['price']:.2f}", f"{total_price:.2f}"])
        
        DATA.append(["Sub Total", "", "", f"{subtotal:.2f}"])
        if discount > 0:
            DATA.append(["Discount", "", "", f"-{discount:.2f}"])
        if tax > 0:
            DATA.append([f"Tax ({tax}%)", "", "", f"{tax_amount:.2f}"])
        DATA.append(["Final Total", "", "", f"{final_total:.2f}"])
        
        # Create PDF
        pdf_filename = f"invoices/bill_{invoice_id}.pdf"
        os.makedirs("invoices", exist_ok=True)
        pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        elements = []
        
        # Company Header
        company_title = Paragraph(f"<b>{company_info.get('name', 'ABC Traders Pvt. Ltd.')}</b>", styles["Title"])
        company_addr = Paragraph(company_info.get('address', '123 Business Street, City Center, Mumbai, India'), styles["Normal"])
        elements.append(company_title)
        elements.append(company_addr)
        elements.append(Spacer(1, 20))
        
        # Invoice Title
        title_style = styles["Heading1"]
        title_style.alignment = 1
        title = Paragraph("INVOICE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Customer Info + Invoice ID
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        customer_info = Paragraph(
            f"<b>Invoice ID:</b> {invoice_id}<br/><b>Customer:</b> {customer_name}<br/><b>Date:</b> {date_str}",
            styles["Normal"]
        )
        elements.append(customer_info)
        elements.append(Spacer(1, 20))
        
        # Table Style
        style = TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ])
        
        table = Table(DATA, style=style)
        elements.append(table)
        
        # Build PDF
        pdf.build(elements)
        
        return jsonify({
            'success': True,
            'message': f'Invoice generated successfully: {pdf_filename}',
            'invoice_id': invoice_id,
            'filename': pdf_filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating invoice: {str(e)}'
        })

@app.route('/download_invoice/<filename>')
def download_invoice(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error downloading invoice: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)