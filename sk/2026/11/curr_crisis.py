import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

H, MIN_YEAR, MAX_YEAR = 1, 1950, 2019
TRAIN_END = 2010
FEATS = ["ca", "rer_dev", "exports", "output", "infl", "credit"]

dlog = lambda s: np.log(s.where(s > 0)).diff()

def construct(g, us_cpi):
    g = g.sort_values("year").set_index("year")
    g = g.reindex(range(int(g.index.min()), int(g.index.max()) + 1))
    g["ISO3"] = g["ISO3"].ffill().bfill()
    idx = g.index

    rer = np.log((g["USDfx"] * us_cpi.reindex(idx) / g["CPI"]).where(lambda s: s > 0))
    rer = rer.replace([np.inf, -np.inf], np.nan)    

    # Rolling 20-year linear trend, using only past/current data
    window = 20
    trend_values = pd.Series(index=idx, dtype=float)
    for i in range(len(rer)):
        sub = rer.iloc[max(0, i - window + 1):i + 1].dropna()
        if len(sub) >= 5:
            p = np.polyfit(sub.index, sub.values, 1)
            trend_values.iloc[i] = np.polyval(p, idx[i])
    rer_dev = rer - trend_values
    
    R = pd.DataFrame({
        "ca":      -g["CA_GDP"],
        "rer_dev": -rer_dev,
        "exports": -dlog(g["exports_USD"]),
        "output":  -dlog(g["rGDP"]),
        "infl":    g["infl"],
        "credit":  dlog(g["M2"]) - dlog(g["nGDP"]),
    }).replace([np.inf, -np.inf], np.nan)

    # Expanding-window standardization (no look-ahead)
    R_scaled = R.apply(
        lambda col: (col - col.expanding(min_periods=5).mean())
        / col.expanding(min_periods=5).std()
    )

    fwd = pd.concat([g["CurrencyCrisis"].shift(-k) for k in range(1, H + 1)], axis=1)
    R_scaled["target"] = fwd.max(axis=1).where(fwd.notna().any(axis=1))
    R_scaled["crisis"] = g["CurrencyCrisis"]
    R_scaled["ISO3"] = g["ISO3"]
    R_scaled["year"] = idx
    return R_scaled.reset_index(drop=True)

def train():

    # ----------------------------- Data -------------------------------
    df = pd.read_csv("/opt/Downloads/gmd/gmd.csv")
    us_cpi = df[df.ISO3 == "USA"].set_index("year")["CPI"]

    # Full feature table (unfiltered) -- used for scoring any country-year
    full = pd.concat([construct(g, us_cpi) for _, g in df.groupby("ISO3")], ignore_index=True)

    # Modelling panel (filtered)
    panel = full[(full.year >= MIN_YEAR) & (full.year <= MAX_YEAR)]
    panel = panel[panel["crisis"] != 1]
    panel = panel.dropna(subset=FEATS + ["target"])

    # ----------------------------- Train / test -----------------------
    train = panel[panel.year <= TRAIN_END].copy()
    test = panel[panel.year > TRAIN_END].copy()

    print(f"Train obs: {len(train)}, Test obs: {len(test)}")
    print("Test target distribution:")
    print(test.target.value_counts())

    Xtr = sm.add_constant(train[FEATS])
    logit = sm.Logit(train["target"], Xtr).fit(
        disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(train.ISO3)[0]}
    )
    print(logit.summary())

    def score(frame):
        return logit.predict(sm.add_constant(frame[FEATS], has_constant="add"))

    train.loc[:, "score"] = score(train)
    test.loc[:, "score"] = score(test)

    print("\nAUC in-sample (train):", roc_auc_score(train.target, train.score))
    print("AUC out-of-time (test):", roc_auc_score(test.target, test.score))

    return logit
    
if __name__ == "__main__": 
    logit = train()



    
