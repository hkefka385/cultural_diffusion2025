import pickle
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# Load the data
def load_data(filepath):
    """Load dataset from a pickle file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

# Preprocess the data
def preprocess_data(df):
    """Handle missing values and prepare the dataframe."""
    df.fillna(0, inplace=True)
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df['target'] = df['target'] - 1
    df['target'] = df['target'].astype(int)
    return df

# Fit the Negative Binomial Regression model
def fit_negative_binomial(df):
    """Fit a Negative Binomial Regression model to the data."""
    formula = 'target ~ ' + ' + '.join(df.drop('target', axis=1).columns)
    model = smf.negativebinomial(formula=formula, data=df).fit(maxiter=5000, method='bfgs')
    return model

# Save the results
def save_results(model, df, output_prefix):
    """Save model coefficients and summary to CSV files."""
    # Save coefficients
    summary_table = model.summary().tables[1]
    df_coef = pd.DataFrame(summary_table.data[1:], columns=summary_table.data[0])
    df_coef.set_index('', inplace=True)
    df_coef['coef'] = df_coef['coef'].astype(float)
    df_coef.to_csv(f'{output_prefix}_coefficients.csv')

    # Save summary
    summary_table2 = model.summary().tables[0]
    data_rows = []
    for row in summary_table2.data:
        cleaned_row = [item.strip() for item in row if item]
        data_rows.append(cleaned_row)
    df_summary = pd.DataFrame(data_rows)
    df_summary.to_csv(f'{output_prefix}_summary.csv', index=False)

    # Save full model as a pickle file
    with open(f'{output_prefix}_model.pickle', 'wb') as f:
        pickle.dump(model, f)

# Main execution
if __name__ == "__main__":
    input_filepath = '****.pickle'  # Input data file
    output_prefix = 'negative_binomial_***'  # Prefix for output files

    # Load and preprocess the data
    data, col_dict = load_data(input_filepath)
    df = preprocess_data(data)

    # Fit the model
    model = fit_negative_binomial(df)

    # Save results
    save_results(model, df, output_prefix)

    print("Negative Binomial Regression completed and results saved.")
