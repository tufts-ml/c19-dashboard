from typing import Dict, Tuple, Set

import numpy as np
import pandas as pd

from constants.column_keys import SCENARIO, DATE_GENERATED, CHART
from constants.paths import PATH_TO_DATA


def get_data() -> Tuple[pd.DataFrame, Dict[str, Set]]:
    """
    Loads the formatted data into the Dashboard.
    :return: The data and control options. Never None.
    """
    df = pd.read_csv(PATH_TO_DATA)
    control_options = get_control_options(df)
    return df, control_options


def get_control_options(df: pd.DataFrame) -> Dict[str, Set]:
    """
    Gets the control options from the dataframe.
    :param df: The dataframe to extrapolate control options from. Cannot be None.
    :return: The control options. Never None.
    """
    possible_scenarios = set(df[SCENARIO].unique())
    possible_scenarios.remove(np.nan)

    possible_dates = set(df[DATE_GENERATED].unique())
    possible_dates.remove(np.nan)

    possible_charts = set([column for column in df.columns.values if column.startswith('n_')])
    return {DATE_GENERATED: possible_dates,
            SCENARIO: possible_scenarios,
            CHART: possible_charts}
