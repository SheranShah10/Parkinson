import os
import markdown
from fpdf import FPDF

def create_pdf(markdown_file, output_pdf):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Create PDF object
    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 15)
            self.cell(0, 10, 'Parkinson\'s Disease Predictive Modeling - Final Clinical Report', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=12)

    # Simplified parsing for the PDF
    lines = md_text.split('\n')
    for line in lines:
        if line.startswith('# '):
            pdf.set_font("helvetica", 'B', 16)
            pdf.ln(5)
            pdf.multi_cell(0, 10, line[2:].strip())
            pdf.set_font("helvetica", size=12)
        elif line.startswith('## '):
            pdf.set_font("helvetica", 'B', 14)
            pdf.ln(3)
            pdf.multi_cell(0, 10, line[3:].strip())
            pdf.set_font("helvetica", size=12)
        elif line.startswith('### '):
            pdf.set_font("helvetica", 'B', 12)
            pdf.ln(2)
            pdf.multi_cell(0, 10, line[4:].strip())
            pdf.set_font("helvetica", size=12)
        elif line.startswith('- ') or line.startswith('* '):
            pdf.multi_cell(0, 8, "  - " + line[2:].replace('*', '').replace('`', ''))
        elif line.startswith('|'):
            # Simple table row rendering
            cols = line.split('|')[1:-1]
            if len(cols) > 0 and '---' not in line:
                col_width = 190 / len(cols)
                for col in cols:
                    text = col.replace('*', '').replace('`', '').strip()
                    pdf.cell(col_width, 10, text, border=1)
                pdf.ln()
        elif line.strip() != '' and '---' not in line:
            clean_line = line.replace('*', '').replace('`', '').replace('$', '').strip()
            clean_line = clean_line.replace('\u2014', '-').replace('\u2013', '-').replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
            pdf.multi_cell(0, 8, clean_line)
        elif line.strip() == '':
            pdf.ln(2)

    pdf.output(output_pdf)
    print(f"Successfully generated {output_pdf}")

if __name__ == '__main__':
    # Using the walkthrough file as source for the report
    source_md = "C:/Users/Sheran/.gemini/antigravity/brain/dbab32c0-3195-48c9-bfb4-60095e19c698/walkthrough.md"
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_pdf = os.path.join(output_dir, "Final_Clinical_Models_Report.pdf")
    create_pdf(source_md, output_pdf)
