import re
import pdfplumber as pmb

def parse_sbi_details(details: str,amount: float) -> dict:
    """
    Parses SBI bank statement Details column.
    Example input:
      'WDL TFR UPI/DR/533853256091/HungerBox/YESB/paytm-8774/UPI'
    """
    details = str(details).strip()
    details_clean = str(details).replace("\n", " ").strip()
    result = {
        "txn_type": "unknown",   # DEP (credit) or WDL (debit)
        "direction": "unknown",  # CR or DR
        "ref_no": "",
        "merchant": "unknown",
        "bank": "",
        "upi_id": "",
        "amount":0.00
    }

    # Detect DEP (deposit/credit) or WDL (withdrawal/debit)
    if details.startswith("DEP"):
        result["txn_type"] = "deposit"
        result["direction"] = "CR"
    elif details.startswith("WDL"):
        result["txn_type"] = "withdrawal"
        result["direction"] = "DR"

    # Extract the UPI portion: UPI/DR|CR/refno/merchant/bank/upi_id
    upi_match = re.search(r'UPI/[A-Z]+/(\d+)/([^/]+)/([^/]+)/([^\s/]+)', details)
    if upi_match:
        result["ref_no"]   = upi_match.group(1)
        result["merchant"] = upi_match.group(2).strip()
        result["bank"]     = upi_match.group(3).strip()
        result["upi_id"]   = upi_match.group(4).strip()
        result["amount"]   = amount
        return result

    ach_match = re.search(
        r'ACHDr\s+[A-Z0-9]+\s+(.+?)(?:\s*-\s*(?:OT|SIP|MF|EMI))?\s*$',
        details_clean
    )
    if ach_match:
        raw = ach_match.group(1).strip()
        # Map known short codes to full names
        merchant_map = {
            "BD Kotak MF":   "Kotak Mutual Fund",
            "Kotak MF":      "Kotak Mutual Fund",
            "ICIPRU":        "ICICI Prudential",
            "HDFCMF":        "HDFC Mutual Fund",
            "SBIMF":         "SBI Mutual Fund",
            "AXISMF":        "Axis Mutual Fund",
            "KOTAKLIFE":     "Kotak Life Insurance",
            "LICPMNT":       "LIC Premium",
        }
        merchant = next(
            (v for k, v in merchant_map.items() if k in raw.upper()), 
            raw
        )
        result["merchant"] = merchant
        result["txn_type"] = "ACH/SIP"
        result["direction"] = "DR"
        result["amount"]   = amount
        return result

    # 3. Interest Credit
    if re.search(r'INTEREST\s+CREDIT', details_clean, re.IGNORECASE):
        result["merchant"] = "Bank Interest"
        result["txn_type"] = "INTEREST"
        result["direction"] = "CR"
        result["amount"]   = amount
        return result
    # 4. ATM Withdrawal
    # Pattern: ATM WDL AT {location} {date}
    atm_match = re.search(
        r'ATM\s+WDL\s+(?:ATM\s+CASH\s+)?(?:AT\s+)?(.+)', 
        details_clean
    )
    if atm_match:
        result["merchant"] = "ATM - " + atm_match.group(1).strip()
        result["txn_type"] = "ATM"
        result["direction"] = "DR"
        result["amount"]   = amount
        return result
    # 5. NEFT / RTGS
    neft_match = re.search(
        r'(?:NEFT|RTGS)[*][\w]+[*][\w\s]+[*]([A-Z][A-Z0-9\s]+?)(?:\s+\d{7,}|\s+AT\s+)',
        details_clean
    )
    if neft_match:
        result["merchant"] = neft_match.group(1).strip()
        result["txn_type"] = "NEFT/RTGS"
        result["direction"] = "CR" if "DEP" in details_clean else "DR"
        result["amount"]   = amount
        return result
    # 6. Cheque
    if re.search(r'CLG|CHEQUE|CHQ', details_clean, re.IGNORECASE):
        result["merchant"] = "Cheque"
        result["txn_type"] = "CHEQUE"
        result["amount"]   = amount
        return result

    # 7.. Direct Bank Transfer — WDL TFR SBIY.../M/ Description ... OF Mr. NAME
    if re.search(r'[A-Z0-9]{10,}[-/]\S*\s+([A-Za-z][A-Za-z\s]+?)\s+\d{7,}', details_clean):
        
        # Try to get recipient name first (most useful)
        name_match = re.search(
            r'OF\s+(?:Mr\.|Mrs\.|Ms\.|M/s\.)?\s*([A-Z][A-Z\s]+?)(?:\s+AT\s+|\s+\d)',
            details_clean
        )
        
        # Fallback to description if no name found
        desc_match = re.search(
            r'/[A-Z]/\s+([A-Za-z][A-Za-z\s]+?)\s+\d{7,}',
            details_clean
        )

        if name_match:
            result["merchant"] = name_match.group(1).strip().title()
        elif desc_match:
            result["merchant"] = desc_match.group(1).strip().title()
        else:
            result["merchant"] = "Bank Transfer"

        result["txn_type"] = "TRANSFER"
        result["direction"] = "DR" if "WDL TFR" in details_clean else "CR"
        result["amount"]   = amount
        return result


    # 8. INB E-mandate — government / corporate auto-debit
    # Pattern: WDL TFR INB E mandate {REF} OF {ENTITY} AT {BRANCH}
    inb_match = re.search(
        r'INB\s+E[\s-]?mandate\s+\d+\s+OF\s+([A-Z][A-Z\s]+?)(?:\s+AT\s+|\s+\d)',
        details_clean,
        re.IGNORECASE
    )
    if inb_match:
        result["merchant"] = inb_match.group(1).strip().title()
        result["txn_type"] = "E-MANDATE"
        result["direction"] = "DR"
        result["amount"]   = amount
        return result

    return result
    

# print(parse_sbi_details("DEBIT ACHDr HDFC00070000003309 ICIPRU 0812202",120.89))

# Function to extract data from PDF file using PDF plumber
def extractPdfData(pdf_path):
    pdf = pmb.open(pdf_path)
    all_text = []

    for page in pdf.pages:
        table = page.extract_table()

        for row in table:
            result = {
            "txn_type": "unknown",   # DEP (credit) or WDL (debit)
            "direction": "unknown",  # CR or DR
            "ref_no": "",
            "merchant": "unknown",
            "bank": "",
            "upi_id": "",
            "amount":0.00
            }

            # Need to check if row[2] is not = None or Empty
            if(row[0] != "unknown"):
                trans_append_in_arry = parse_sbi_details(row[2], row[4] if row[4] not in ("-", "") else row[5])
            if(trans_append_in_arry["ref_no"] == ""):
                result["ref_no"] = row[2]
                result["amount"] = row[4] if row[4] != "-" else row[5]
                print(result)
            else:
                print(trans_append_in_arry)
                # else:
                #     result["ref_no"] = row[2]
                #     result["amount"] = row[4] if row[4] != "-" else row[5]
                #     all_text.append(result)
                

    # print(all_text)
                    
                    # SANTI\nKU



    

extractPdfData("C://Users//shubdasgupta//Expense Tracker//Expense-Tracker//Expense-Tracker//ai_model//SHUBH04082003.pdf")


