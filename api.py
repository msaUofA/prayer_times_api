import pandas as pd
from flask import Flask, jsonify, request, Response
from datetime import datetime

file_path: str = 'Edmonton Prayer Times - 2025 IMS 3.csv'
data: pd.DataFrame = pd.read_csv(file_path)

months: list[str] = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

month_starts: pd.Index = data[data.iloc[:, 1].isin(months)].index

months_data: dict[str, pd.DataFrame] = {}

for i, start in enumerate(month_starts):
    month_name: str = data.iloc[start, 1]
    end: int = month_starts[i + 1] if i + 1 < len(month_starts) else len(data)
    month_df: pd.DataFrame = data.iloc[start + 1:end].copy()
    month_df.columns = ['Day', 'Date', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Extra']
    month_df = month_df.drop(columns=['Extra']).dropna(subset=['Date'])
    month_df['Date'] = pd.to_numeric(month_df['Date'], errors='coerce').dropna().astype(int)
    months_data[month_name] = month_df

app: Flask = Flask(__name__)

@app.route('/prayer-times', methods=['GET'])
def get_prayer_times() -> Response:
    month_i: int = request.args.get('month', type=int)
    day: int = request.args.get('day', type=int)

    if not month_i or not day:
        today: datetime = datetime.now()
        month_i, day = today.month, today.day

    if month_i not in range(1, 13):
        return jsonify({'error': 'Invalid month'}), 400

    month: str = months[month_i]
    month_data: pd.DataFrame = months_data.get(month)
    
    if month_data is None:
        return jsonify({'error': 'No data available for the provided month'}), 404

    prayer_times: pd.DataFrame = month_data[month_data['Date'] == day]

    if prayer_times.empty:
        return jsonify({'error': 'No data available for the provided day'}), 404

    result: dict[str, object] = prayer_times[['Day', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']].to_dict(orient='records')[0]
    return jsonify(result)

@app.route('/prayer-times/<int:month>/<int:day>', methods=['GET'])
def get_prayer_times2(month: int, day: int) -> Response:
    if month not in range(1, 13):
        return jsonify({'error': 'Invalid month'}), 400

    month_name: str = months[month]
    month_data: pd.DataFrame = months_data.get(month_name)

    if month_data is None:
        return jsonify({'error': 'No data available for the provided month'}), 404

    prayer_times: pd.DataFrame = month_data[month_data['Date'] == day]

    if prayer_times.empty:
        return jsonify({'error': 'No data available for the provided day'}), 404

    result: dict[str, object] = prayer_times[['Day', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']].to_dict(orient='records')[0]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
