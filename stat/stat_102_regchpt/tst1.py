import numpy as np
import pandas as pd
import bayes_segmented 

# =====================================================================
# 1. CONFIGURATION & LOAD RAW DATA
# =====================================================================
NUM_BLOCKS = 3  
NUM_TAUS = NUM_BLOCKS - 1
np.random.seed(42)

df = pd.read_csv('../../compscieng/compscieng_app20cfit/cave.csv')
X = df['Temp'].values
Y = df['C'].values
N = len(df)

print(f"Loaded {N} data points from cave.csv.")

# =====================================================================
# 2. RUN SAMPLER
# =====================================================================
trace_taus, trace_alphas, trace_betas, trace_sigmas = bayes_segmented.metropolis_sampler(
    X, Y, 
    num_blocks=NUM_BLOCKS,
    iterations=50000, 
    burn_in=20000, 
    proposal_width_tau=0.3,    
    proposal_width_alpha=0.15,  
    proposal_width_beta=0.01,   
    proposal_width_sigma=0.05   
)

# =====================================================================
# 3. RESULTS & GOODNESS-OF-FIT
# =====================================================================
print("\n--- INFERENCE RESULTS ---")
for i in range(NUM_TAUS):
    print(f"Estimated Tau {i+1} (Timeline Index): {np.mean(trace_taus[:, i]):.2f} ± {np.std(trace_taus[:, i]):.2f}")
print("")
for i in range(NUM_BLOCKS):
    print(f"Block {i+1} -> Alpha (Intercept): {np.mean(trace_alphas[:, i]):.3f} | Beta (Slope): {np.mean(trace_betas[:, i]):.3f} | Sigma (Noise): {np.mean(trace_sigmas[:, i]):.3f}")

print("\n--- GOODNESS-OF-FIT METRICS ---")
est_taus = np.mean(trace_taus, axis=0)
est_alphas = np.mean(trace_alphas, axis=0)
est_betas = np.mean(trace_betas, axis=0)
est_sigmas = np.mean(trace_sigmas, axis=0)

# Call modular log_likelihood from the routine package
max_log_lik = bayes_segmented.log_likelihood(est_taus, est_alphas, est_betas, est_sigmas, X, Y)

num_params = (NUM_BLOCKS - 1) + NUM_BLOCKS + NUM_BLOCKS + NUM_BLOCKS
aic = 2 * num_params - 2 * max_log_lik
bic = num_params * np.log(N) - 2 * max_log_lik

print(f"Maximized Log-Likelihood: {max_log_lik:.2f}")
print(f"Total Parameters (k):     {num_params}  (Expanded to 4M - 1 due to intercepts)")
print(f"AIC Score:                {aic:.2f}")
print(f"BIC Score:                {bic:.2f} <-- Best for identifying true block count")
