import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gumbel_r
import seaborn as sns

# Setting visual style for a professional look
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Arial']

def solve_hydrology_risk():
    # 1. Generate Simulated Rainfall Data
    # Assume the true parameters: mu (location) = 50, beta (scale) = 10
    # In reality, this data would come from historical observations.
    np.random.seed(42)
    data = gumbel_r.rvs(loc=50, scale=10, size=100)
    
    # 2. Maximum Likelihood Estimation (MLE)
    # The .fit() method in scipy uses MLE to estimate the parameters
    # mu_hat is the location parameter, beta_hat is the scale parameter
    mu_hat, beta_hat = gumbel_r.fit(data)
    
    print(f"--- Gumbel Distribution Parameters (MLE) ---")
    print(f"Location Parameter (μ): {mu_hat:.4f}")
    print(f"Scale Parameter (β): {beta_hat:.4f}\n")

    # 3. Return Period Analysis
    # The Return Period T is defined as: T = 1 / (1 - F(x))
    # Therefore, the Cumulative Distribution Function (CDF) F(x) = 1 - 1/T
    # The Return Level x_T = mu - beta * ln(-ln(F(x)))
    return_periods = [20, 50, 100]
    return_levels = {}

    print(f"--- Return Period Rainfall Depths (mm) ---")
    for T in return_periods:
        # Calculate the probability for the specific return period
        prob = 1 - (1 / T)
        # Calculate the return level using the Percent Point Function (Inverse of CDF)
        level = gumbel_r.ppf(prob, loc=mu_hat, scale=beta_hat)
        return_levels[T] = level
        print(f"{T}-year return period: {level:.2f} mm")

    # 4. Visualization
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram of simulated data (Density=True for comparison with PDF)
    sns.histplot(data, bins=15, kde=False, stat="density", color='skyblue', 
                 alpha=0.6, label='Simulated Annual Max Rainfall')

    # Plot the fitted Gumbel PDF
    x = np.linspace(min(data) - 10, max(data) + 50, 1000)
    pdf_fitted = gumbel_r.pdf(x, loc=mu_hat, scale=beta_hat)
    ax.plot(x, pdf_fitted, 'r-', lw=2.5, label=f'Fitted Gumbel PDF\n(μ={mu_hat:.2f}, β={beta_hat:.2f})')

    # Mark Return Periods on the plot
    colors = ['green', 'orange', 'red']
    for (T, level), color in zip(return_levels.items(), colors):
        ax.axvline(level, color=color, linestyle='--', alpha=0.8, 
                   label=f'{T}-yr Level: {level:.1f} mm')

    # Aesthetics
    ax.set_title('Hydrological Risk Modeling: Gumbel Distribution Fitting', fontsize=14, fontweight='bold')
    ax.set_xlabel('Annual Maximum Daily Rainfall (mm)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.legend(frameon=True, fontsize=10)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    solve_hydrology_risk()
    
