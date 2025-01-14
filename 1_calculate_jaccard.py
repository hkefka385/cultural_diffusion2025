import pickle
import pandas as pd
from collections import defaultdict

def load_data(filepath):
    with open(filepath, mode='rb') as f:
        return pickle.load(f)


def calculate_jaccard(data):
    """Calculate Jaccard indices from the given data."""
    all_key = list(data.keys())
    all_key_list = [list(data[key]) for key in all_key]

    language_counts = defaultdict(int)
    pair_counts = defaultdict(int)

    for sublist in all_key_list:
        # Get unique languages in the sublist
        unique_languages = list(set(sublist))

        # Count occurrences of each language
        for language in unique_languages:
            language_counts[language] += 1

        # Count occurrences of language pairs
        for i in range(len(unique_languages)):
            lang1 = unique_languages[i]
            for j in range(i + 1, len(unique_languages)):
                lang2 = unique_languages[j]
                pair_counts[tuple(sorted([lang1, lang2]))] += 1

    # Create a matrix to store pair counts
    languages = list(language_counts.keys())
    matrix = pd.DataFrame(0, index=languages, columns=languages)

    for (lang1, lang2), count in pair_counts.items():
        matrix.loc[lang1, lang2] = count
        matrix.loc[lang2, lang1] = count  # Ensure symmetry

    # Calculate Jaccard indices
    jaccard_distance = pd.DataFrame(index=languages, columns=languages)
    for lang1 in languages:
        for lang2 in languages:
            if lang1 == lang2:
                jaccard_distance.loc[lang1, lang2] = 0
            else:
                intersection = matrix.loc[lang1, lang2]
                union = language_counts[lang1] + language_counts[lang2] - intersection
                jaccard_distance.loc[lang1, lang2] = intersection / union if union > 0 else 0

    return jaccard_distance

def save_jaccard(jaccard_distance, output_path):
    """Save the Jaccard indices to a CSV file."""
    jaccard_distance.to_csv(output_path)

def main():
    # Path to the input data and output file
    input_filepath = 'index.pickle'
    output_filepath = 'jaccard_distance***.csv'

    # Load data
    data = load_data(input_filepath)

    # Calculate Jaccard indices
    jaccard_distance = calculate_jaccard(data)

    # Save the results
    save_jaccard(jaccard_distance, output_filepath)

if __name__ == "__main__":
    main()
