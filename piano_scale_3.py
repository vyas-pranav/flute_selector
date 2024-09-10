import numpy as np
import matplotlib.pyplot as plt

# Western chromatic scale
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Good and bad notes binary code series
good_bad_code = np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1])  # Example series

# Function to convert Hindustani notes to Western pitches
interval_map = {
    "S": 0,  "r": 1,  "R": 2,  "g": 3,  "G": 4,
    "m": 5,  "M": 6,  "P": 7,
    "d": 8, "D": 9, "n": 10, "N": 11
}

def hindustani_to_western(scale_notes, base_pitch_index):
    return [(base_pitch_index + interval_map[note]) % 12 for note in scale_notes]

def evaluate_pitch(pitch_index, western_scale_pitches):\
    #create a list from 0 to 11 representing the pitch scale
    pitch_scale = [i for i in range(12)]

    # Shift the pitch scale to the base pitch index
    shifted_base_scale = pitch_scale[pitch_index:] + pitch_scale[:pitch_index]

    # Create a binary list for the chromatic scale
    chromatic_scale = [1 if i in western_scale_pitches else 0 for i in shifted_base_scale]
    chromatic_array = np.array(chromatic_scale)
    
    # Element-wise multiplication with good_bad_code
    result_array = chromatic_array * good_bad_code
    return np.sum(result_array)

#function to calculate indian notation form binary series
def calculate_indian_notation(binary_series):
    indian_notation = []
    for i in range(12):
        if binary_series[i] == 1:
            #get the indian note form the interval_map
            indian_note = [key for key, value in interval_map.items() if value == i][0]
            indian_notation.append(indian_note)
    return indian_notation

#function to calculate what does Sa should mean while playing the scale
def calculate_sa_means(pitch, base_pitch_index):
    #get the position of the base pitch in the chromatic scale that starts from the pitch
    pitch_scale = [i for i in range(12)]
    shifted_pitch_scale = pitch_scale[pitch:] + pitch_scale[:pitch]
    sa_index = shifted_pitch_scale.index(base_pitch_index)

    #get the indian note that should be played as Sa
    sa_note = [key for key, value in interval_map.items() if value == sa_index][0]

    return sa_note

#plotting the results
def plot_keys_for_all_pitches(results, base_pitch_index, hindustani_scale):
    # Extract pitches and binary series from results
    pitches = [result[0] for result in results]
    binary_series_matrix = [result[1] for result in results]
    indian_notations = [result[3] for result in results]
    sa_means = [result[4] for result in results]
    
    # Number of base pitches
    num_pitches = len(pitches)
    num_notes = len(binary_series_matrix[0])

    # Set up the figure and axis, make two columns for better visualization
    fig, ax = plt.subplots((num_pitches + 1) // 2, 2, figsize=(15, 5 * (num_pitches + 1) // 2))

    # Handle case when there's only one row of subplots
    if num_pitches == 1:
        ax = np.array([ax])

    # Plot the binary series for each base pitch
    for i in range(num_pitches):
        row = i // 2
        col = i % 2

        # Annotate the Indian notation and Sa means right above each plot
        indian_notation = ", ".join(indian_notations[i])
        sa_mean = sa_means[i]
        ax[row, col].text(1, 1.1, f"Indian notation: {indian_notation}",
                         horizontalalignment='right', verticalalignment='baseline',
                         fontsize=12, transform=ax[row, col].transAxes)
        ax[row, col].text(0, 1.1, f"Raga's S = {sa_means[i]}",
                         horizontalalignment='left', verticalalignment='baseline',
                         fontsize=12, transform=ax[row, col].transAxes)
        #write the score of the base pitch
        ax[row, col].text(0, 1.5, f"Score: {results[i][2]}", horizontalalignment='left', verticalalignment='baseline', fontsize=12, transform=ax[row, col].transAxes)

        # Display the binary series with halved size
        im = ax[row, col].imshow([binary_series_matrix[i]], cmap='Oranges', aspect='equal', interpolation='none')

        ax[row, col].set_xlabel(f"Instrument base pitch: {pitches[i]}", fontsize=14, labelpad=3)

        ax[row, col].set_xticks(range(num_notes))

        # Set the x-axis labels to the shifted chromatic scale
        pitch_ind = notes.index(pitches[i])
        shifted_scale = [notes[(pitch_ind + j) % 12] for j in range(12)]
        ax[row, col].set_xticklabels(shifted_scale)

        # Adjust the size of the y-axis to accommodate the halved size
        ax[row, col].set_ylim(-0.5, 0.5)

        #turn off vertical ticks and labels
        ax[row, col].tick_params(axis='y', which='both', left=False, right=False)
        ax[row, col].set_yticks([])

        #make vertical lines to separate the notes
        for j in range(1, 12):
            ax[row, col].axvline(j - 0.5, color='black', lw=0.5)

        #write indian notations in the center of the pixels of the plot
        for j in range(12):
            indian_note = [key for key, value in interval_map.items() if value == j][0]
            ax[row, col].text(j, 0, indian_note, ha='center', va='center', fontsize=12)


    #add a super title to the figure showing the input Hindustani scale and base pitch
    fig.suptitle(f"Keys to play the scale {', '.join(hindustani_scale)} at pitch {notes[base_pitch_index]}", fontsize=16)

    # Adjust layout to avoid overlapping
    plt.show()


# Ask user for scale notes in Hindustani classical style
print("\nInput the notes of the scale in Hindustani classical style (keys: S, r, R, g, G, m, M, P, d, D, n, N).")
scale_input = input("Enter the notes separated by spaces: ").split()

# Validate and convert Hindustani notes to Western pitches
scale_intervals = []
for note in scale_input:
    if note in interval_map:
        scale_intervals.append(interval_map[note])
    else:
        print(f"Invalid note: {note}. Please enter valid Hindustani notes (S, r, R, g, G, m, M, P, d, D, n, N).")
        exit()

# Convert the scale to Western pitches relative to the base pitch (which is just a reference)
base_pitch = input("\nEnter the base pitch in Western notation (e.g., C, D#, A): ").strip()

if base_pitch not in notes:
    print("Invalid base pitch. Please choose from the listed pitches.")
    exit()

base_pitch_index = notes.index(base_pitch)
western_scale_pitches = hindustani_to_western(scale_input, base_pitch_index)

#print the scale in Western notation
print(f"\nScale notes in Western notation based on {base_pitch}:")
print(", ".join([notes[pitch] for pitch in western_scale_pitches]))

# Evaluate all possible base pitches
results = []
for i in range(12):
    pitch = notes[i]
    western_pitches = western_scale_pitches
    score = evaluate_pitch(i, western_pitches)
    binary_series = [1 if (i + j) % 12 in western_pitches else 0 for j in range(12)]
    indian_notes = calculate_indian_notation(binary_series)
    sa_means = calculate_sa_means(i, base_pitch_index)
    results.append((pitch, binary_series, score, indian_notes, sa_means))

# Sort results by score in descending order
results.sort(key=lambda x: x[2], reverse=True)

# Display results
print("\nBase notes and corresponding series of 0s and 1s sorted by the number of good notes:")
for pitch, binary_series, score, indian_notes, sa_means in results:
    print(f"\nBase pitch for instrument: {pitch}")
    print(f"Keys to play series: {binary_series}")
    print(f"Score (number of good notes): {score}")
    print(f"Indian notation: {indian_notes}")
    print(f"Raga's S = {sa_means} on instrument")

# Plot the keys for all base pitches
plot_keys_for_all_pitches(results, base_pitch_index, scale_input)
