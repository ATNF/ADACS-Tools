CSIMPATH=$ASKAP_ROOT/Code/Components/Synthesis/synthesis/current/apps/
CSIM=${CSIMPATH}/csimulator.sh
MERGE=${CSIMPATH}/msmerge.sh

#clean up the measurement sets
rm -rf chan_*.ms
rm -rf continuum.ms
rm -rf full_band.ms
rm -rf multi_chan*.ms

#run the simulator
mpiexec -n 2 $CSIM -c chan_1.in
mpiexec -n 2 $CSIM -c chan_2.in
mpiexec -n 2 $CSIM -c chan_3.in
mpiexec -n 2 $CSIM -c chan_4.in
mpiexec -n 2 $CSIM -c chan_5.in
mpiexec -n 2 $CSIM -c chan_6.in
mpiexec -n 2 $CSIM -c chan_7.in
mpiexec -n 2 $CSIM -c chan_8.in

mpiexec -n 2 $CSIM -c chan_1a.in
mpiexec -n 2 $CSIM -c chan_2a.in
mpiexec -n 2 $CSIM -c chan_3a.in
mpiexec -n 2 $CSIM -c chan_4a.in
mpiexec -n 2 $CSIM -c chan_5a.in
mpiexec -n 2 $CSIM -c chan_6a.in
mpiexec -n 2 $CSIM -c chan_7a.in
mpiexec -n 2 $CSIM -c chan_8a.in


$MERGE -o multi_chan_00.ms chan_1.ms chan_2.ms chan_3.ms chan_4.ms chan_5.ms chan_6.ms chan_7.ms chan_8.ms 

$MERGE -o multi_chan_01.ms chan_1a.ms chan_2a.ms chan_3a.ms chan_4a.ms chan_5a.ms chan_6a.ms chan_7a.ms chan_8a.ms 

cp -r multi_chan_00.ms full_band.ms
#cflag -c flag.in

