import streamlit as st
from datetime import date
import re

st.set_page_config(page_title="Annexure-C Generator", layout="centered")
st.title("🚛 Vehicle Load Entry & Annexure-C Receipt")

COMPANY_NAME = "SHRIRAM ENTERPRISES(11/800)"

st.subheader("📝 Vehicle Load Entry Form")

# Persistent container count state
if "num_containers" not in st.session_state:
    st.session_state.num_containers = 1

# Dynamic container count input
st.session_state.num_containers = st.number_input(
    "How many containers?", min_value=1, step=1, value=st.session_state.num_containers
)

shipping_bill_no = st.text_input("Shipping Bill Number", placeholder="SB123456")
shipping_bill_date = st.date_input("Shipping Bill Date", value=date.today())

container_details = []
for i in range(st.session_state.num_containers):
    st.markdown(f"**Container {i+1} Details:**")
    cnum = st.text_input(f"Container Number {i+1}", key=f"cnum{i}")
    csize = st.selectbox(f"Container Size {i+1}", ["20 ft", "40 ft", "Other"], key=f"csize{i}")
    seal = st.text_input(f"Seal Number {i+1}", key=f"seal{i}")
    sdate = st.date_input(f"Date of Sealing {i+1}", value=date.today(), key=f"sdate{i}")
    container_details.append((cnum, csize, seal, sdate))

gross_weight = st.number_input("Gross Weight (in kg)", min_value=0.0, step=0.1)
net_weight = st.number_input("Net Weight (in kg)", min_value=0.0, step=0.1)
package_type = st.text_input("Package Type (e.g. Boxes, Cartons, Bags)")

submit = st.button("Generate Annexure-C")

# Vehicle number validation
def is_valid_indian_vehicle(number):
    return re.fullmatch(r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}", number) is not None

if submit:
    if net_weight > gross_weight:
        st.error("❌ Net weight cannot be more than gross weight.")
    else:
        # Container rows
        container_rows = ""
        for cnum, csize, seal, sdate in container_details:
            container_rows += f"<tr><td>{cnum}</td><td>{csize}</td><td>{seal}</td><td>{sdate.strftime('%d-%m-%Y')}</td></tr>"


        receipt_html = f"""
        <style>
            .receipt {{
                font-family: 'Segoe UI', sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                font-size: 14px;
                line-height: 1.6;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 10px;
            }}
            table, th, td {{
                border: 1px solid black;
                padding: 4px;
                text-align: center;
            }}
            .bold {{ font-weight: bold; }}
            .section-title {{
                font-size: 16px;
                margin-top: 15px;
                font-weight: bold;
            }}
            .print-btn {{
                text-align: center;
                margin-top: 20px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 16px;
                background-color: #006666;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #004d4d;
            }}
        </style>

        <div class="receipt" id="receipt">
            <h3 style="text-align:center">ANNEXURE-C</h3>
            <p style="text-align:center">DATA TO BE ENTERED BY EXAMINING OFFICER/P.O. WHEN<br>EXPORT GOODS ARE BROUGHT FOR EXAMINATION</p>

            <div style="display:flex; justify-content:space-between;">
                <div>1. Shipping Bill No.: <span class="bold" style="font-size:24px;">{shipping_bill_no}</span></div>
                <div>Date: <span class="bold">{shipping_bill_date.strftime('%d-%m-%Y')}</span></div>
            </div>

            <div>2. If Clubbing, No. and date of other S/Bs: __________________________</div>
            <div>3. Date of receipt of full consignment: __________________________</div>
            <div>4. (a) Vessel Name: ____________________</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(b) Shipping Line: ____________________</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(c) Steamer Agent Name: ____________________</div>
            <div>5. Freight and insurance charges</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(i) Freight Value: _____________ Currency: _____________</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(ii) Insurance Value: _____________ Currency: _____________</div>
            <div>6. Total No. of Packages: ____________________</div>
            <div>7. Types of pkgs (Boxes/Cartons/Bags etc.): <span class="bold">{package_type}</span></div>
            <div>8. Numbers marked on the pkgs (1-25 etc.): ____________________</div>
            <div>9. Gross weight (in Kgs): <span class="bold">{gross_weight:.2f} Kg</span></div>
            <div>10. Net weight (in Kgs): <span class="bold">{net_weight:.2f} Kg</span></div>

            <div class="section-title">11. Container particulars</div>
            <table>
                <tr><th>Container No.</th><th>Size</th><th>Seal No.</th><th>Date of Sealing</th></tr>
                {container_rows}
            </table>

            <div>12. Name of the sealing agency: __________________________</div>
            <div>13. Whether factory stuffed: (Yes/No): No</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(i) If yes, whether sample accompanies: (Yes/No): No</div>
            <div>&nbsp;&nbsp;&nbsp;&nbsp;(ii) Factory name and address: __________________________</div>

            <p>I/We declare that the particulars given above are true and correct.</p>
            <div>Name of the Exporter/CHA: <span class="bold">{COMPANY_NAME}</span></div>
            <div>ID No of authorised signatory of CHA: __________________________</div>
            <div>Date: __________________</div>
            <div>Goods arrived. Verified the number of packages and marks and numbers thereon and found to be as declared.</div>

            <div style="margin-top: 30px;">
                <div>Name of the Examining Officer (P.O.): __________________________</div>
                <div>Signature of the Examining Officer (P.O.): __________________________</div>
            </div>

            <p style="margin-top: 15px; font-size: 12px;"><b>Note:</b> For factory/CFS stuffed containers, gross weight given in Sl. No. 9 should be exclusive of the weight of the container.</p>
        </div>

        <div class="print-btn">
            <button onclick="printDiv()">🖨️ Print Annexure-C</button>
        </div>

        <script>
        function printDiv() {{
            var printContents = document.getElementById('receipt').innerHTML;
            var originalContents = document.body.innerHTML;
            document.body.innerHTML = printContents;
            window.print();
            document.body.innerHTML = originalContents;
        }}
        </script>
        """
        st.components.v1.html(receipt_html, height=1600, scrolling=True)
