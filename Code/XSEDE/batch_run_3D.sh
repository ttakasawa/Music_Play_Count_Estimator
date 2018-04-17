#!/bin/bash
#SBATCH -N 1
#SBATCH -p GPU
#SBATCH --gres=gpu:p100:2
#SBATCH -t 8:00:00
#SBATCH --ntasks-per-node 28
#SBATCH -r DS340Music_3D

#load packages your project depends on module load opencv/3.2.0
module load cuda/9.0
module load python3/3.5.2_gcc_mkl
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/packages/cuda/9.0/extras/CUPTI/lib64

#move to project directory
cd $HOME/ds340

#run your executable
python3 keras_model.py 3
