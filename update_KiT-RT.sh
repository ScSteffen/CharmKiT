cd KiT-RT
git checkout hot_fix_mpi_deploy
git pull origin
cd tools/singularity
singularity exec kit_rt.sif ./install_kitrt_singularity.sh
cd ../../../