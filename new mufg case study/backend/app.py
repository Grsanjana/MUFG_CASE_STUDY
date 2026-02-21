from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variable to store current dataset
current_dataset = None

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_dataset
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file based on extension
        filename = file.filename.lower()
        
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Store dataset
        current_dataset = df
        
        # Convert full dataset to JSON
        full_data = df.to_dict('records')
        
        # Replace NaN with None for JSON serialization
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        # Also create preview (first 100 rows) for display
        preview_data = full_data[:100]
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'preview': preview_data,  # For display
            'data': full_data  # Full dataset for operations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clean/remove-null', methods=['POST'])
def remove_nulls():
    try:
        data = request.json.get('data', [])
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame(data)
        
        # Remove rows with any null values
        df_cleaned = df.dropna()
        
        # Convert full dataset and clean NaN values
        full_data = df_cleaned.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df_cleaned),
            'columns': list(df_cleaned.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/clean/remove-duplicate', methods=['POST'])
def remove_duplicates():
    try:
        data = request.json.get('data', [])
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame(data)
        
        # Remove duplicate rows
        df_cleaned = df.drop_duplicates()
        
        # Convert full dataset and clean NaN values
        full_data = df_cleaned.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df_cleaned),
            'columns': list(df_cleaned.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/clean/rename-columns', methods=['POST'])
def rename_columns():
    try:
        data = request.json.get('data', [])
        rename_map = request.json.get('rename_map', {})
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame(data)
        
        # Rename columns
        df_renamed = df.rename(columns=rename_map)
        
        # Convert full dataset to dict and clean NaN values
        full_data = df_renamed.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df_renamed),
            'columns': list(df_renamed.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/clean/change-datatypes', methods=['POST'])
def change_datatypes():
    try:
        data = request.json.get('data', [])
        dtype_map = request.json.get('dtype_map', {})
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame(data)
        
        # Convert data types
        for col, dtype in dtype_map.items():
            if col in df.columns:
                try:
                    if dtype == 'date':
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif dtype == 'int':
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                    elif dtype == 'float':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif dtype == 'string':
                        df[col] = df[col].astype(str)
                except Exception as e:
                    # If conversion fails, keep original
                    pass
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/clean/trim-whitespaces', methods=['POST'])
def trim_whitespaces():
    try:
        data = request.json.get('data', [])
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame(data)
        
        # Trim whitespaces from string columns
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                # Replace 'nan' string with None
                df[col] = df[col].replace('nan', None)
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value) or value == 'nan' or value == 'None':
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/math/sum', methods=['POST'])
def calculate_sum():
    try:
        data = request.json.get('data', [])
        column = request.json.get('column')
        
        df = pd.DataFrame(data)
        
        if column not in df.columns:
            return jsonify({'error': f'Column {column} not found'}), 400
        
        # Convert to numeric, ignoring errors
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        result = numeric_values.sum()
        
        return jsonify({
            'success': True,
            'value': float(result) if not pd.isna(result) else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/math/average', methods=['POST'])
def calculate_average():
    try:
        data = request.json.get('data', [])
        column = request.json.get('column')
        
        df = pd.DataFrame(data)
        
        if column not in df.columns:
            return jsonify({'error': f'Column {column} not found'}), 400
        
        # Convert to numeric, ignoring errors
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        result = numeric_values.mean()
        
        return jsonify({
            'success': True,
            'value': float(result) if not pd.isna(result) else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/math/min', methods=['POST'])
def calculate_min():
    try:
        data = request.json.get('data', [])
        column = request.json.get('column')
        
        df = pd.DataFrame(data)
        
        if column not in df.columns:
            return jsonify({'error': f'Column {column} not found'}), 400
        
        # Convert to numeric, ignoring errors
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        result = numeric_values.min()
        
        return jsonify({
            'success': True,
            'value': float(result) if not pd.isna(result) else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/math/max', methods=['POST'])
def calculate_max():
    try:
        data = request.json.get('data', [])
        column = request.json.get('column')
        
        df = pd.DataFrame(data)
        
        if column not in df.columns:
            return jsonify({'error': f'Column {column} not found'}), 400
        
        # Convert to numeric, ignoring errors
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        result = numeric_values.max()
        
        return jsonify({
            'success': True,
            'value': float(result) if not pd.isna(result) else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/math/count', methods=['POST'])
def calculate_count():
    try:
        data = request.json.get('data', [])
        column = request.json.get('column')
        
        df = pd.DataFrame(data)
        
        if column not in df.columns:
            return jsonify({'error': f'Column {column} not found'}), 400
        
        # Count non-null values
        result = df[column].notna().sum()
        
        return jsonify({
            'success': True,
            'value': int(result)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/math/add', methods=['POST'])
def calculate_add():
    try:
        data = request.json.get('data', [])
        column1 = request.json.get('column1')
        column2 = request.json.get('column2')
        result_column = request.json.get('result_column', f'{column1}_plus_{column2}')
        
        df = pd.DataFrame(data)
        
        if column1 not in df.columns or column2 not in df.columns:
            return jsonify({'error': 'One or both columns not found'}), 400
        
        # Convert to numeric
        col1 = pd.to_numeric(df[column1], errors='coerce')
        col2 = pd.to_numeric(df[column2], errors='coerce')
        
        # Perform addition
        df[result_column] = col1 + col2
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/math/subtract', methods=['POST'])
def calculate_subtract():
    try:
        data = request.json.get('data', [])
        column1 = request.json.get('column1')
        column2 = request.json.get('column2')
        result_column = request.json.get('result_column', f'{column1}_minus_{column2}')
        
        df = pd.DataFrame(data)
        
        if column1 not in df.columns or column2 not in df.columns:
            return jsonify({'error': 'One or both columns not found'}), 400
        
        # Convert to numeric
        col1 = pd.to_numeric(df[column1], errors='coerce')
        col2 = pd.to_numeric(df[column2], errors='coerce')
        
        # Perform subtraction
        df[result_column] = col1 - col2
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/math/multiply', methods=['POST'])
def calculate_multiply():
    try:
        data = request.json.get('data', [])
        column1 = request.json.get('column1')
        column2 = request.json.get('column2')
        result_column = request.json.get('result_column', f'{column1}_times_{column2}')
        
        df = pd.DataFrame(data)
        
        if column1 not in df.columns or column2 not in df.columns:
            return jsonify({'error': 'One or both columns not found'}), 400
        
        # Convert to numeric
        col1 = pd.to_numeric(df[column1], errors='coerce')
        col2 = pd.to_numeric(df[column2], errors='coerce')
        
        # Perform multiplication
        df[result_column] = col1 * col2
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/math/divide', methods=['POST'])
def calculate_divide():
    try:
        data = request.json.get('data', [])
        column1 = request.json.get('column1')
        column2 = request.json.get('column2')
        result_column = request.json.get('result_column', f'{column1}_divided_by_{column2}')
        
        df = pd.DataFrame(data)
        
        if column1 not in df.columns or column2 not in df.columns:
            return jsonify({'error': 'One or both columns not found'}), 400
        
        # Convert to numeric
        col1 = pd.to_numeric(df[column1], errors='coerce')
        col2 = pd.to_numeric(df[column2], errors='coerce')
        
        # Perform division (handle division by zero)
        df[result_column] = col1.div(col2.replace(0, pd.NA))
        
        # Convert full dataset and clean NaN values
        full_data = df.to_dict('records')
        for record in full_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': list(df.columns),
            'data': full_data
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/advanced/pl/gross-profit', methods=['POST'])
def calculate_gross_profit():
    try:
        data = request.json.get('data', [])
        revenue_col = request.json.get('revenue_column')
        cost_col = request.json.get('cost_column')
        
        df = pd.DataFrame(data)
        
        if revenue_col not in df.columns or cost_col not in df.columns:
            return jsonify({'error': 'Required columns not found'}), 400
        
        # Convert to numeric
        revenue = pd.to_numeric(df[revenue_col], errors='coerce')
        cost = pd.to_numeric(df[cost_col], errors='coerce')
        
        # Calculate gross profit
        gross_profit = revenue - cost
        total_gross_profit = gross_profit.sum()
        
        return jsonify({
            'success': True,
            'total_revenue': float(revenue.sum()),
            'total_cost': float(cost.sum()),
            'total_gross_profit': float(total_gross_profit)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/advanced/pl/net-profit', methods=['POST'])
def calculate_net_profit():
    try:
        data = request.json.get('data', [])
        revenue_col = request.json.get('revenue_column')
        cost_col = request.json.get('cost_column')
        tax_col = request.json.get('tax_column')
        
        df = pd.DataFrame(data)
        
        if revenue_col not in df.columns or cost_col not in df.columns or tax_col not in df.columns:
            return jsonify({'error': 'Required columns not found'}), 400
        
        # Convert to numeric
        revenue = pd.to_numeric(df[revenue_col], errors='coerce')
        cost = pd.to_numeric(df[cost_col], errors='coerce')
        tax = pd.to_numeric(df[tax_col], errors='coerce')
        
        # Calculate gross profit and net profit
        gross_profit = revenue - cost
        net_profit = gross_profit - tax
        
        return jsonify({
            'success': True,
            'total_revenue': float(revenue.sum()),
            'total_cost': float(cost.sum()),
            'total_tax': float(tax.sum()),
            'total_gross_profit': float(gross_profit.sum()),
            'total_net_profit': float(net_profit.sum())
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/advanced/pl/monthly', methods=['POST'])
def calculate_monthly_pl():
    try:
        data = request.json.get('data', [])
        revenue_col = request.json.get('revenue_column')
        cost_col = request.json.get('cost_column')
        date_col = request.json.get('date_column')
        
        df = pd.DataFrame(data)
        
        if revenue_col not in df.columns or cost_col not in df.columns or date_col not in df.columns:
            return jsonify({'error': 'Required columns not found'}), 400
        
        # Convert date column
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Convert to numeric
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors='coerce')
        df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce')
        
        # Remove rows with invalid dates
        df = df.dropna(subset=[date_col])
        
        # Extract month-year
        df['month'] = df[date_col].dt.to_period('M').astype(str)
        
        # Group by month
        monthly = df.groupby('month').agg({
            revenue_col: 'sum',
            cost_col: 'sum'
        }).reset_index()
        
        monthly['profit'] = monthly[revenue_col] - monthly[cost_col]
        
        monthly_data = []
        for _, row in monthly.iterrows():
            monthly_data.append({
                'month': row['month'],
                'revenue': float(row[revenue_col]),
                'cost': float(row[cost_col]),
                'profit': float(row['profit'])
            })
        
        return jsonify({
            'success': True,
            'monthly_data': monthly_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/advanced/pl/quarterly', methods=['POST'])
def calculate_quarterly_pl():
    try:
        data = request.json.get('data', [])
        revenue_col = request.json.get('revenue_column')
        cost_col = request.json.get('cost_column')
        date_col = request.json.get('date_column')
        
        df = pd.DataFrame(data)
        
        if revenue_col not in df.columns or cost_col not in df.columns or date_col not in df.columns:
            return jsonify({'error': 'Required columns not found'}), 400
        
        # Convert date column
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Convert to numeric
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors='coerce')
        df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce')
        
        # Remove rows with invalid dates
        df = df.dropna(subset=[date_col])
        
        # Extract quarter
        df['quarter'] = df[date_col].dt.quarter
        df['year'] = df[date_col].dt.year
        df['quarter_label'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
        
        # Group by quarter
        quarterly = df.groupby('quarter_label').agg({
            revenue_col: 'sum',
            cost_col: 'sum'
        }).reset_index()
        
        quarterly['profit'] = quarterly[revenue_col] - quarterly[cost_col]
        
        quarterly_data = []
        for _, row in quarterly.iterrows():
            quarterly_data.append({
                'quarter': row['quarter_label'],
                'revenue': float(row[revenue_col]),
                'cost': float(row[cost_col]),
                'profit': float(row['profit'])
            })
        
        # Sort by quarter
        quarterly_data.sort(key=lambda x: x['quarter'])
        
        return jsonify({
            'success': True,
            'quarterly_data': quarterly_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/transformed', methods=['POST'])
def download_transformed():
    """
    Download the transformed dataset as an Excel file.
    Expects JSON body: { "data": [...] }
    """
    try:
        data = request.json.get('data', [])
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='TransformedData')
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name='transformed_dataset.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

