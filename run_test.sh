#!/usr/bin/env bash


#python ./build_infiles.py
#source ./build_sim.sh

runner="mpiexec "

CSIMPATH=$ASKAP_ROOT/Code/Components/Synthesis/synthesis/current/apps/
IMAGEPATH=$ASKAP_ROOT/Code/Components/CP/askap_imager/current/apps/
ANALYSIS=$ASKAP_ROOT/Code/Components/Analysis/analysis/current/apps/
CSIM=${CSIMPATH}/csimulator.sh
MERGE=${CSIMPATH}/msmerge.sh
IMAGER=${IMAGEPATH}/imager.sh
LINMOS=${CSIMPATH}/linmos-mpi.sh
SELAVY=${ANALYSIS}/selavy.sh
rm -rf *.cont
rm -rf *.restored
rm -rf *.fits

for beam in b1 b2; do
#    $runner -n 2 $IMAGER -c ./AWproject-${beam}.in 1> image${beam}.log
    $runner -n 2 $IMAGER -c ./WProject-${beam}.in 1> image${beam}.log
    $runner -n 1 $LINMOS -c ./linmos-individual-${beam}.in 1> linmos.log
    $runner -n 1 $SELAVY -c ./selavy-${beam}.in 1> selavy.log
    cp selavy-results.txt results-${beam}.txt
    $runner -n 1 $SELAVY -c ./selavy-c-${beam}.in 1> selavy.log
    cp selavy-results.txt results-c-${beam}.txt

done

$runner -n 1 $LINMOS -c ./linmos-b1b2.in 1> linmos.log
$runner -n 1 $SELAVY -c ./selavy-b1b2.in 1> selavy.log
cp selavy-results.txt results-b1b2.txt
$runner -n 1 $LINMOS -c ./linmos-c-b1b2.in 1> linmos.log
$runner -n 1 $SELAVY -c ./selavy-c-b1b2.in 1> selavy.log
cp selavy-results.txt results-c-b1b2.txt
