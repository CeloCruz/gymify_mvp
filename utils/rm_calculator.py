import pandas as pd
import numpy as np

def calculate_1rm(weight1, reps1, rir1=0, weight2=None, reps2=None, rir2=0):
    """
    Calculates 1RM and estimates rep maxes from 2RM to 10RM, optionally averaging
    with a second sample. Uses the Brzycki formula and incorporates RIR.


    Args:
    weight1: Weight lifted in the first set (lbs or kg).
    reps1: Repetitions performed in the first set.
    rir1: Reps in reserve for the first set (default: 0).
    weight2: (Optional) Weight lifted in the second set.
    reps2: (Optional) Repetitions performed in the second set.
    rir2: Reps in reserve for the second set (default: 0).


    Returns:
    A tuple containing:
    - 1RM: The calculated or averaged 1RM (float).
    - rep_max_table: A pandas DataFrame with estimated 2RM to 10RM.
    """
    def _calculate_1rm_brzycki(weight, reps, rir):
        """Helper function to calculate 1RM using Brzycki formula with RIR."""
        effective_reps = reps + rir
        if effective_reps <= 0:  # Handle cases where reps + rir is zero or negative
            return None  # Or raise an exception: raise ValueError("Reps plus RIR must be greater than zero.")
        return float(weight / (1.0278 - 0.0278 * effective_reps))

    # Calculate 1RM for the first set
    rm1 = _calculate_1rm_brzycki(weight1, reps1, rir1)
    if rm1 is None:
        raise ValueError("Las repeticiones más el RIR tienen que ser superior a 0.")

    # Calculate 1RM for the second set, if provided
    rm2 = None
    if weight2 is not None and reps2 is not None:
        rm2 = _calculate_1rm_brzycki(weight2, reps2, rir2)

    # Average 1RM if two sets are provided
    if rm2 is not None:
        one_rm = (rm1 + rm2) / 2
    else:
        one_rm = rm1

    # Estimate rep maxes from 2RM to 10RM using the calculated 1RM
    rep_maxes = []
    for r in range(2, 11):
        est_weight = round(one_rm * (1.0278 - 0.0278 * r), 2)
        percent_rm = round((est_weight / one_rm) * 100, 2)
        rep_maxes.append({"Reps": r, "Peso": np.round(est_weight,1), "% RM": np.round(percent_rm,1)})

    rep_max_table = pd.DataFrame(rep_maxes)
    rep_max_table.set_index("Reps", inplace=True)  # Set 'Reps' as the index

    return one_rm, rep_max_table

