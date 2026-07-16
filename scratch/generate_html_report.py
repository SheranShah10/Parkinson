import os
import markdown

def generate_report():
    source_md = "C:/Users/Sheran/.gemini/antigravity/brain/dbab32c0-3195-48c9-bfb4-60095e19c698/walkthrough.md"
    
    with open(source_md, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Extract the leaderboard sections we want for the final report
    report_md = """# Parkinson's Disease Predictive Modeling: Final Clinical Report
*Comprehensive overview of Tier 1, Tier 2, and Tier 3 Clinical Model Benchmarks.*

---

""" + md_text

    # Convert to HTML
    html_content = markdown.markdown(report_md, extensions=['tables', 'fenced_code'])
    
    # Wrap in a beautiful CSS template for printing
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Final Clinical Models Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 2rem;
            }}
            h1, h2, h3 {{ color: #2c3e50; }}
            h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 14px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            blockquote {{
                background: #fdf6e3;
                border-left: 5px solid #e74c3c;
                margin: 1.5em 10px;
                padding: 1em 15px;
            }}
            .print-button {{
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            @media print {{
                .print-button {{ display: none; }}
                body {{ padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <button class="print-button" onclick="window.print()">🖨️ Save as PDF</button>
        {html_content}
    </body>
    </html>
    """

    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    html_path = os.path.join(output_dir, "Final_Clinical_Models_Report.html")
    md_path = os.path.join(output_dir, "Final_Clinical_Models_Report.md")
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(styled_html)
        
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Report saved to {html_path} and {md_path}")

if __name__ == '__main__':
    generate_report()
