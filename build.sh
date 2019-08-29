#########################
## NVIDIA repositories ##
#########################

#########################
# ## Conda Dependencies ##
#########################

conda install -y -c conda-forge automake make cmake libtool pkg-config cupy

conda install -y pytest-asyncio

#########################
# cudf
#########################

git clone https://github.com/rapidsai/cudf
cd cudf
export CUDA_HOME=/usr/local/cuda-9.2
export CUDACXX=$CUDA_HOME/bin/nvcc
conda env create --name cudf_dev_92 --file conda/environments/cudf_dev_cuda9.2.yml
conda activate cudf_dev_92
./build.sh
cd ..

#########################
# dask
#########################

git clone https://github.com/rapidsai/dask
cd dask
pip install -e .
cd ..

#########################
# dask-cuda
#########################

git clone https://github.com/rapidsai/dask-cuda
cd dask-cuda
pip install -e .
cd ..

#########################
# ## UCX ##
#########################

git clone https://github.com/openucx/ucx
cd ucx
git remote add Akshay-Venkatesh git@github.com:Akshay-Venkatesh/ucx.git
git remote update Akshay-Venkatesh
git checkout ucx-cuda
./autogen.sh
mkdir build
cd build
../configure --prefix=$CONDA_PREFIX --enable-debug --with-cuda=$CUDA_HOME --enable-mt --disable-cma CPPFLAGS="-I//$CUDA_HOME/include"
make -j install
cd ../..

#########################
# ucx-py
#########################

git clone https://github.com/rapidsai/ucx-py
cd ucx-py
export UCX_PATH=$CONDA_PREFIX
make install

#########################
# You should be done! Test the result of your build with
#########################

pytest -v

