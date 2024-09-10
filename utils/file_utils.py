import pandas as pd


def export_to_csv(data, filepath):


    """
    Generate a CSV report from the DataFrame and save it to a file.
    :param data:
    :param filepath:
    :return:
    """

    # report_columns = ['Symbol', 'Date', 'Close Price', 'Daily Weighting', 'Algo-RiskMetricName',
    #                   'Algo-RiskMetric-ReturnValue-Daily']

    report_columns  = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Create a DataFrame with only the required columns
    report_data = data[report_columns]

    # Save the DataFrame to a CSV file
    report_data.to_csv(filepath, index=False)

    print(f"CSV report generated successfully at: {filepath}")


def export_to_html(data, filepath):

    """
    Generate an HTML report from the DataFrame and save it to a file.
    :param data:
    :param filepath:
    :return:
    """

    # report_columns = ['Symbol', 'Date', 'Close Price', 'Daily Weighting', 'Algo-RiskMetricName',
    #                   'Algo-RiskMetric-ReturnValue-Daily']

    report_columns  = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Create a DataFrame with only the required columns
    report_data = data[report_columns]

    # Convert DataFrame to HTML with additional CSS styling for clear visibility
    html_content = report_data.to_html(index=False, justify='center')

    # Add custom styles for better visibility
    html_content = f"""
    <html>
    <head>
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th, td {{
        padding: 10px;
        text-align: center;
        border: 1px solid black;
    }}
    th {{
        background-color: #f2f2f2;
    }}
    </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    with open(filepath, 'w') as file:
        file.write(html_content)

    print(f"HTML report generated successfully at: {filepath}")


def generate_basic_excel_report(data, filepath):
    """
    Generate a basic Excel report from the DataFrame and save it to a file.
    :param data:
    :param filepath:
    :return:
    """

    # report_columns = ['Symbol', 'Date', 'Close Price', 'Daily Weighting', 'Algo-RiskMetricName',
    #                   'Algo-RiskMetric-ReturnValue-Daily']
    report_columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Create a DataFrame with only the required columns
    report_data = data[report_columns]

    # Save the DataFrame to an Excel file
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        report_data.to_excel(writer, sheet_name='Financial Report', index=False)

        # Access the XlsxWriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets['Financial Report']

        # Set the column width for better visibility
        for column in report_columns:
            column_length = max(report_data[column].astype(str).map(len).max(), len(column)) + 2
            col_idx = report_columns.index(column)
            worksheet.set_column(col_idx, col_idx, column_length)

    print(f"Excel report generated successfully at: {filepath}")
