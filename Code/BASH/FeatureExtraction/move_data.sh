# DO NOT RUN AS A SCRIPT

for D in `find . -maxdepth 1 -type d`
do
    if [ -d $D/split/ ]; then
	mkdir $D/fft
	mkdir $D/tempo
        cd $D/split/
        mv *fft.npy ../fft
        mv *tempo.npy ../tempo
        cd ..
        cd ..
    fi
done
