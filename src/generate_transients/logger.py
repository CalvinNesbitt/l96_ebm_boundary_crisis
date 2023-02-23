"Function to log the result of a tipping experiment."

from pathlib import Path
import pandas as pd

mac_home_dir = Path("/Users/cfn18")
home_dir = Path.home()

if Path.home() == Path("/Users/cfn18"):
    results_file = Path(
        "/Users/cfn18/Documents/PhD-Work/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/data/transient_lifetimes.csv"
    )
else:
    results_file = Path(
        "/rds/general/user/cfn18/home/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/data/transient_lifetimes.csv"
    )


# Ensure we have a dataframe to write into.


def make_csv_file():
    df = pd.DataFrame(columns=["S", "dissapearing_attractor", "tipping_time"])
    df.to_csv(results_file)
    return


# Function for logging results

if not results_file.exists():
    print(f"Making CSV file at {str(results_file)}\n")
    make_csv_file()


def log_result(S: float, dissapearing_attractor: str, tipping_time: float):
    result_data = pd.DataFrame(
        {"S": [S], "dissapearing_attractor": [dissapearing_attractor], "tipping_time": [tipping_time]}
    )
    result_data.to_csv(results_file, mode="a", header=False)
    print(f"Logged S={S:.3f} at {results_file}\n\n")
    return
