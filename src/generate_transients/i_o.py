from pathlib import Path

if Path.home() == Path("/Users/cfn18"):
    transient_ic_dir = Path(
        "/Users/cfn18/Documents/PhD-Work/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/data/transient_ics"
    )
else:
    transient_ic_dir = Path(
        "/rds/general/user/cfn18/home/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/data/transient_ics"
    )

if not transient_ic_dir.exists():
    transient_ic_dir.mkdir(parents=True)
    print(f"Made directory at {str(transient_ic_dir)}\n\n")
