# Make directory to copy model in to, submit job from there
NOW=$(date +"%Y-%m-%d-%T")
run_directory="$EPHEMERAL/L96-EBM-DET/Tipping-Points/Run-Dirs/$NOW"
mkdir -p $run_directory
cp $HOME/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/bin/determine_tipping_points/cluster/*.sh $run_directory
cp -r $HOME/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/src $run_directory
cd $run_directory
qsub determine_tipping_points.sh
