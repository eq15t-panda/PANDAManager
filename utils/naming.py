import os
from datetime import datetime


def make_run_dir(data_dir: str, meas: str, sample: str) -> str:
    """
    Create and return a unique dated run directory.
    Keep a consistent file naming system across all notebooks.

    Structure: data_dir/meas/date_sample_001/

    :param data_dir: root data directory
    :param meas: measurement type, used as subfolder
    :param sample: sample name
    :return: formatted run directory path
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    meas_dir = os.path.join(data_dir, meas)
    run_name = f"{date_str}_{sample}"

    idx = 1
    while os.path.exists(os.path.join(meas_dir, f"{run_name}_{idx:03d}")):
        idx += 1

    run_dir = os.path.join(meas_dir, f"{run_name}_{idx:03d}")
    os.makedirs(run_dir)

    print(f"Saving data to: {run_dir}")
    return run_dir