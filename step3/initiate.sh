mkdir job tools
ln -s ../../libsvm-3.18/svm-predict .
ln -s ../../libsvm-3.18/svm-train .
ln -s ../../libsvm-3.18/svm-scale .
cd tools
ln -s ../../../libsvm-3.18/tools/* .
rm grid.py
cp ../../../libsvm-3.18/tools/grid.py .
cd ..
