#PBS -l walltime=00:30:00
#PBS -l select=1:ncpus=8:mem=96gb
#PBS -N Generate_Transients
#PBS -J 1-10000

module load anaconda3/personal
source activate l96_ebm_det
date
cd "$PBS_O_WORKDIR"
python src/generate_transients/main.py $PBS_ARRAY_INDEX