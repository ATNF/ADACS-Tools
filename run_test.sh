#!/usr/bin/env bash


#python ./build_infiles.py
#source ./build_sim.sh

runner="mpiexec "

CSIMPATH=$ASKAP_ROOT/Code/Components/Synthesis/synthesis/current/apps/
IMAGEPATH=$ASKAP_ROOT/Code/Components/CP/askap_imager/current/apps/
CSIM=${CSIMPATH}/csimulator.sh
MERGE=${CSIMPATH}/msmerge.sh
IMAGER=${IMAGEPATH}/imager.sh


rm -rf *.cont
rm -rf *.restored
rm -rf *.fits

for beam in b1 b2; do
    $runner -n 2 $IMAGER -c ./AWproject-${beam}.in 1> image${beam}.log
#    $runner -n 1 linmos-mpi -c ./linmos-individual-${beam}.in 1> linmos.log
#    $runner -n 1 selavy -c ./selavy-${beam}.in 1> selavy.log
#    cp selavy-results.txt results-${beam}.txt
done

#$runner -n 1 linmos-mpi -c ./linmos-b1b2.in 1> linmos.log
#$runner -n 1 selavy -c ./selavy-b1b2.in 1> selavy.log
#cp selavy-results.txt results-b1b2.txt
