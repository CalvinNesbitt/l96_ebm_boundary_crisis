#PBS -l walltime=00:30:00
#PBS -l select=1:ncpus=8:mem=96gb
#PBS -N Determine_tipping
#PBS -J 1-10

module load anaconda3/personal
source activate l96_ebm_det
date
cd "$PBS_O_WORKDIR"
python src/tipping_points/main.py $PBS_ARRAY_INDEX