#setup python environment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

#compile gnuplot
tar -xzvf gnuplot-4.6.5.tar.gz
cd gnuplot-4.6.5/
./configure
make
cd ..

#compile Vienna RNA
tar -xzvf ViennaRNA-2.1.8.tar.gz
cd ViennaRNA-2.1.8/
./configure --with-python
make
cd interfaces/Python
python setup.py install
cd ../../../

#compile libsvm
tar -xzvf libsvm-3.18.tar.gz
cd libsvm-3.18
make
cd ..

#Create output folders
cd step3
mkdir ani && cd ani
../initiate.sh
cd .. && mkdir pla && cd pla
../initiate.sh
cd .. && mkdir g3 && cd g3
../initiate.sh
cd ..
mkdir zjob
