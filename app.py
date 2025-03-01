import streamlit as st
import pandas as pd
from bcb import currency
import plotly.graph_objects as go
import datetime as dt

st.set_page_config(page_title='Currency Exchange Rates', page_icon='💱', layout='wide')

#currencies = currency.get_currency_list()
#currencies = currencies[currencies['exclusion_date'].isnull()]
#currency_codes = currencies['symbol'].unique().tolist()
currency_codes = ['AUD', 'CAD', 'CHF', 'DKK', 'EUR', 'GBP', 'JPY', 'NOK', 'SEK', 'USD']

# Function to fetch and clean currency data
def get_data(currency_code, start, end):
    # Download currency data using bcb
    data = currency.get(currency_code, start=start, end=end)
    data['date'] = pd.to_datetime(data.index, format='%Y-%m-%d')
    data = data.melt(id_vars='date', var_name='currency', value_name='value')
    return data

def plot_chart(data, currencies):
    fig = go.Figure()
    for currency in currencies:
        fig.add_trace(
        go.Scatter(x=data[data['currency'] == currency]['date'],
                   y=data[data['currency'] == currency]['value'],
                   mode='lines',
                   name=currency)
        )
    fig.update_layout(
        title=f'Currency to BRL',
        xaxis_title='Date',
        yaxis_title='BRL',
        hovermode = 'x unified'
    )
    return fig


# Main page rendering function
def main_page():
    st.title('Currency Exchange Rates')

    # Get the currency code from the user
    currency_code = st.sidebar.multiselect(
        "Select currency",
        currency_codes,
        default=['USD', 'EUR']
        )
    start_date = st.sidebar.date_input('Start date', pd.to_datetime('2024-01-01'), format='DD/MM/YYYY')
    end_date = st.sidebar.date_input('End date', pd.to_datetime('2024-12-31'), format='DD/MM/YYYY', max_value=dt.datetime.today())

    if currency_code is not None:
        df = get_data(currency_code, start_date, end_date)
    st.session_state.data = df
    fig = plot_chart(st.session_state.data, currency_code)
    st.plotly_chart(fig, use_container_width=False)
    st.write('Source: Banco Central do Brasil')
    st.sidebar.download_button(
        "Download data as CSV",
        st.session_state.data.to_csv(index=False),
        "data.csv"
    )


def main():
    main_page()

if __name__ == '__main__':
    main()