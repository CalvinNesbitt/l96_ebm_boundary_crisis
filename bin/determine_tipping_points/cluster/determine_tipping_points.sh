#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=8:mem=96gb
#PBS -N Determine_tipping
#PBS -J 1-400

module load anaconda3/personal
source activate l96_ebm_det
date
cd "$PBS_O_WORKDIR"
python src/tipping_points/main.py $PBS_ARRAY_INDEX