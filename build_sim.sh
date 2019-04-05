CSIM=csimulator
MERGE=msmerge

#clean up the measurement sets
rm -rf chan_*.ms
rm -rf continuum.ms
rm -rf full_band.ms
rm -rf multi_chan*.ms

#run the simulator
infiles=`ls -1 chan*.in`
mergeline="$MERGE "

for infile in $infiles
do
mpiexec -n 2 -oversubscribe $CSIM -c $infile
inname=$(basename "$infile")
outname=${inname%.*}

if [ -d "askapsdp-3504.ms" ] 
then
	mergeline="msmerge askapsdp-3504.ms ${outname}.ms "
        $mergeline
	rm -rf askapsdp-3504.ms
	mv out.ms askapsdp-3504.ms

else
	mv ${outname}.ms askapsdp-3504.ms
fi

done

