import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd


def main():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 7)
    # List of dates
    dates = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) \
             for i in range((end_date - start_date).days + 1)]

    load_dotenv()

    key = os.getenv('API_KEY')
    url_history = "https://api.apilayer.com/currency_data/historical"

    headers = {
        "apikey": key
    }
    # List with responses
    data = []

    for date in dates:

        params = {
            'date': date
        }

        response = requests.get(url_history, headers=headers, params=params)

        if response.status_code != 200:
            break
        else:
            data.append(response.json()['quotes'])

    else:
        df = pd.DataFrame(data)
        # Change index names
        df.index = dates
        # cut USD from columns names
        df.columns = [col[3:] for col in df.columns]
        df = df.iloc[:, :10]
        df.to_csv('data.csv', index=False)
        print(df)


if __name__ == '__main__':
    main()
