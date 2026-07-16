import os

def generate_custom_report():
    # We will generate a report structured exactly like the provided PDF example
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Parkinson's Disease Predictive Modeling - Model Performance Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.4;
                color: #000;
                max-width: 950px;
                margin: 0 auto;
                padding: 2rem;
            }
            h1.title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            h2 {
                font-size: 18px;
                font-weight: bold;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            h3 {
                font-size: 14px;
                font-weight: bold;
                font-style: italic;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            h4 {
                font-size: 13px;
                font-weight: bold;
                font-style: italic;
                margin-top: 15px;
                margin-bottom: 5px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                font-size: 12px;
            }
            th, td {
                border: 1px solid #000;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                font-weight: normal;
            }
            .print-button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            @media print {
                .print-button { display: none; }
                body { padding: 0; }
            }
        </style>
    </head>
    <body>
        <button class="print-button" onclick="window.print()">🖨️ Save as PDF</button>
        
        <h1 class="title">Parkinson's Disease Predictive Modeling Performance & Class-Level Accuracy Report</h1>

        <h2>1. Summary Performance Table</h2>
        <table>
            <thead>
                <tr>
                    <th>Architecture Category</th>
                    <th>Source Model</th>
                    <th>Classification Acc</th>
                    <th>Classification F1</th>
                    <th>Regression R2</th>
                    <th>Regression RMSE</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>**Traditional ML**</td>
                    <td>Gradient Boosting</td>
                    <td>0.783</td>
                    <td>0.630</td>
                    <td>0.694</td>
                    <td>7.925</td>
                </tr>
                <tr>
                    <td>**Traditional ML**</td>
                    <td>CatBoost</td>
                    <td>0.785</td>
                    <td>0.611</td>
                    <td>0.694</td>
                    <td>7.923</td>
                </tr>
                <tr>
                    <td>**Traditional ML**</td>
                    <td>Logistic/ElasticNet</td>
                    <td>0.759</td>
                    <td>0.625</td>
                    <td>0.656</td>
                    <td>8.415</td>
                </tr>
                <tr>
                    <td>**Tabular Deep Learning**</td>
                    <td>FTTransformer</td>
                    <td>-</td>
                    <td>-</td>
                    <td>0.640</td>
                    <td>8.598</td>
                </tr>
                <tr>
                    <td>**Tabular Deep Learning**</td>
                    <td>SAINT</td>
                    <td>-</td>
                    <td>-</td>
                    <td>0.615</td>
                    <td>8.867</td>
                </tr>
                <tr>
                    <td>**Temporal Deep Learning**</td>
                    <td>LSTM</td>
                    <td>0.760</td>
                    <td>0.614</td>
                    <td>0.588</td>
                    <td>9.856</td>
                </tr>
                <tr>
                    <td>**Temporal Deep Learning**</td>
                    <td>GRU</td>
                    <td>0.757</td>
                    <td>0.604</td>
                    <td>0.605</td>
                    <td>9.651</td>
                </tr>
                <tr>
                    <td>**Temporal Deep Learning**</td>
                    <td>TemporalTransformer</td>
                    <td>0.742</td>
                    <td>0.613</td>
                    <td>0.260</td>
                    <td>13.211</td>
                </tr>
            </tbody>
        </table>

        <h2>2. Detailed Tier-Level Performance Metrics</h2>

        <h3>1. Tier 1: Traditional Machine Learning Models</h3>
        
        <h4>Classification Head (Target: NHY Stage)</h4>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Accuracy (Mean)</th>
                    <th>Balanced Acc</th>
                    <th>F1 Macro (Mean)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Gradient Boosting</td><td>0.783</td><td>0.609</td><td>0.630</td></tr>
                <tr><td>Logistic Regression</td><td>0.759</td><td>0.614</td><td>0.625</td></tr>
                <tr><td>CatBoost</td><td>0.785</td><td>0.588</td><td>0.611</td></tr>
                <tr><td>MLPClassifier</td><td>0.747</td><td>0.594</td><td>0.609</td></tr>
                <tr><td>AdaBoost</td><td>0.751</td><td>0.603</td><td>0.608</td></tr>
                <tr><td>LightGBM</td><td>0.780</td><td>0.578</td><td>0.600</td></tr>
                <tr><td>XGBoost</td><td>0.779</td><td>0.576</td><td>0.594</td></tr>
                <tr><td>Random Forest</td><td>0.789</td><td>0.533</td><td>0.528</td></tr>
            </tbody>
        </table>

        <h4>Regression Head (Target: NP3TOT Motor Severity)</h4>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>RMSE (Mean)</th>
                    <th>MAE (Mean)</th>
                    <th>R2 (Mean)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>CatBoost Regressor</td><td>7.923</td><td>5.807</td><td>0.694</td></tr>
                <tr><td>Gradient Boosting</td><td>7.925</td><td>5.803</td><td>0.694</td></tr>
                <tr><td>Extra Trees Regressor</td><td>7.985</td><td>5.808</td><td>0.690</td></tr>
                <tr><td>Random Forest</td><td>8.013</td><td>5.855</td><td>0.688</td></tr>
                <tr><td>LightGBM Regressor</td><td>8.038</td><td>5.860</td><td>0.685</td></tr>
                <tr><td>ElasticNet</td><td>8.415</td><td>6.468</td><td>0.656</td></tr>
                <tr><td>XGBoost Regressor</td><td>8.455</td><td>6.166</td><td>0.652</td></tr>
                <tr><td>Linear Regression</td><td>29.547</td><td>6.899</td><td>-11.198 (Unstable)</td></tr>
            </tbody>
        </table>

        <br><br> <!-- Page Break simulation -->

        <h3>2. Tier 2: Tabular Deep Learning Models (Zero-Day Architectures)</h3>
        
        <h4>Regression Head (Target: NP3TOT Motor Severity)</h4>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>RMSE</th>
                    <th>R2 Score</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>FTTransformer</td><td>8.598</td><td>0.640</td></tr>
                <tr><td>SAINT</td><td>8.867</td><td>0.615</td></tr>
                <tr><td>TabNet</td><td>9.446</td><td>0.565</td></tr>
                <tr><td>WideDeep</td><td>9.461</td><td>0.555</td></tr>
            </tbody>
        </table>
        
        <br><br>

        <h3>3. Tier 3: Temporal Sequence Models (Longitudinal Progression)</h3>
        
        <h4>Classification Head (Target: NHY Stage)</h4>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>F1 Macro</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>LSTM</td><td>0.760</td><td>0.614</td></tr>
                <tr><td>TemporalTransformer</td><td>0.742</td><td>0.613</td></tr>
                <tr><td>GRU</td><td>0.757</td><td>0.604</td></tr>
                <tr><td>CNN-LSTM</td><td>0.769</td><td>0.603</td></tr>
                <tr><td>BiLSTM</td><td>0.759</td><td>0.585</td></tr>
                <tr><td>TCN</td><td>0.753</td><td>0.581</td></tr>
                <tr><td>Transformer</td><td>0.723</td><td>0.573</td></tr>
            </tbody>
        </table>

        <h4>Regression Head (Target: NP3TOT Motor Severity)</h4>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>RMSE</th>
                    <th>R2 Score</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>GRU</td><td>9.651</td><td>0.605</td></tr>
                <tr><td>BiLSTM</td><td>9.676</td><td>0.603</td></tr>
                <tr><td>LSTM</td><td>9.856</td><td>0.588</td></tr>
                <tr><td>CNN-LSTM</td><td>10.071</td><td>0.570</td></tr>
                <tr><td>Transformer</td><td>10.598</td><td>0.524</td></tr>
                <tr><td>TCN</td><td>10.878</td><td>0.497</td></tr>
                <tr><td>TemporalTransformer</td><td>13.211</td><td>0.260</td></tr>
            </tbody>
        </table>

    </body>
    </html>
    """

    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    html_path = os.path.join(output_dir, "Structured_Performance_Report.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Report saved to {html_path}")

if __name__ == '__main__':
    generate_custom_report()
