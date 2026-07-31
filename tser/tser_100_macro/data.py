import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web

def fetch_and_prepare_macro_data(start_year=1990):
    today = datetime.datetime.now()
    start = datetime.datetime(start_year, 1, 1)
    end = datetime.datetime(today.year, today.month, today.day)
    
    cols = [
        "ARGBCAGDPBP6",       # Balance of Payments (BOP % GDP)
        "ARGCPALTT01GPM",     # CPI Index (Monthly CPI)
        "CRDQARBPUBIS",       # Domestic Credit
        "MKTGDPARA646NWDB",   # Nominal GDP
        "RBARBIS",            # Real Effective Exchange Rate (XCH)
        "GGNLBAARA188N",      # Government Net Borrowing/Lending (% GDP)
        "MYAGM2ARM189N",      # Money Supply M2
        "SLUEM1524ZSARG"      # Unemployment Rate
    ]
    
    print("Fetching FRED macroeconomic data...")
    df = web.DataReader(cols, 'fred', start, end)
    df.columns = ["bop", "cpi", "domcred", "gdp", "xch", "govdebt", "m2", "unemploy"]
    df = df[df.index <= '2025-12-31'].copy()

    # Load External Annual Interest Rates & Anchor
    print("Loading external interest rate dataset (arg_real_ir.csv)...")
    df_ir = pd.read_csv('arg_real_ir.csv')
    
    df['real_ir_anchor'] = np.nan
    for _, row in df_ir.iterrows():
        yr = int(row['year'])
        anchor_date = f"{yr}-07-01"
        if anchor_date in df.index:
            df.loc[anchor_date, 'real_ir_anchor'] = row['real_ir']

    # Use Forward-Fill (.ffill()) to prevent look-ahead bias from linear interpolation
    df['real_ir'] = df['real_ir_anchor'].ffill().bfill()

    # Interpolate FRED series
    df = df.interpolate(method='linear')

    # Compute Macro Transformations
    print("Calculating macro transformations...")
    # 1. Money Supply Growth (% log change)
    df['m2_diff'] = np.log(df['m2'] / df['m2'].shift(1)) * 100.0
    
    # 2. Monthly CPI Inflation Rate (% log change) -> USED AS LEVEL (NOT DOUBLE DIFFERENCED)
    df['inf_diff'] = np.log(df['cpi'] / df['cpi'].shift(1)) * 100.0
    
    # 3. Monthly Exchange Rate Depreciation Rate -> USED AS LEVEL (NOT DOUBLE DIFFERENCED)
    # Negative log change of REER (Positive value = Peso depreciation)
    df['xch_diff'] = -np.log(df['xch'] / df['xch'].shift(1)) * 100.0

    # 4. First differences for Balance of Payments and Interest Rates
    df['bop_diff'] = df['bop'].diff()
    df['ir_diff']  = df['real_ir'].diff()

    # Drop NaNs created by lag/shift operations
    df_clean = df.dropna(subset=['m2_diff', 'inf_diff', 'xch_diff', 'bop_diff', 'ir_diff']).copy()
    
    export_cols = ['bop_diff', 'xch_diff', 'ir_diff', 'inf_diff', 'm2_diff']
    return df_clean[export_cols]

if __name__ == "__main__":
    df_clean = fetch_and_prepare_macro_data()
    df_clean.to_csv('arg_final.csv')
    print("Preprocessing completed successfully. Data exported to 'arg_final.csv'.")
