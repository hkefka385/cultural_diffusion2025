import numpy as np
import pandas as pd
from scipy.optimize import minimize
import pickle

# Load data
def load_data(filepath):
    """Load the dataset from a pickle file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

# Define the Hawkes Process log-likelihood function
def hawkes_log_likelihood(params, events, T, num_marks):
    mu = params[0]
    alpha_0 = params[1:1+num_marks**2].reshape(num_marks, num_marks)
    beta = params[-1]

    log_likelihood = 0
    for sample_idx, (marks, times) in enumerate(events):
        n_events = len(times)
        if n_events == 0:
            continue

        mark_indices = np.array([mark_to_index[mark] for mark in marks])

        # Baseline intensity contribution
        log_likelihood += n_events * np.log(mu)
        log_likelihood -= mu * T

        # Excitation contribution
        for i in range(n_events):
            excitation = 0
            for j in range(i):
                alpha_ij = alpha_0[mark_indices[j], mark_indices[i]]
                excitation += alpha_ij * np.exp(-beta * (times[i] - times[j]))
            log_likelihood += np.log(mu + excitation)

    return -log_likelihood

# Fit the Hawkes Process model
def fit_hawkes_process(events, T, num_marks, init_params):
    """Fit the Hawkes Process model using optimization."""
    result = minimize(
        fun=hawkes_log_likelihood,
        x0=init_params,
        args=(events, T, num_marks),
        method='L-BFGS-B',
        bounds=[(1e-4, None)] * len(init_params),
        options={'disp': True}
    )
    return result

# Save results
def save_results(result, output_prefix):
    """Save the Hawkes Process model parameters and evaluation metrics."""
    params = result.x
    pd.DataFrame(params, columns=['Value']).to_csv(f'{output_prefix}_parameters.csv', index=False)

    with open(f'{output_prefix}_model.pickle', 'wb') as f:
        pickle.dump(result, f)

# Main function
def main():
    input_filepath = '***.pickle'  # Input data
    output_prefix = 'hawkes_process_***'    # Output file prefix

    # Load data
    data = load_data(input_filepath)
    events, metadata = data['events'], data['metadata']

    # Hawkes Process parameters
    T = metadata['end_time']
    num_marks = metadata['num_marks']
    init_params = np.random.rand(1 + num_marks**2 + 1)  # Initialize parameters

    # Fit model
    result = fit_hawkes_process(events, T, num_marks, init_params)

    # Save results
    save_results(result, output_prefix)

    print("Hawkes Process modeling completed and results saved.")

if __name__ == "__main__":
    main()
