scp /media/diego/QData/techarticles/models.tgz ubuntu@18.194.147.93:/media/diego/QData/techarticles
ssh ubuntu@18.194.147.93 'pushd /media/diego/QData/techarticles; tar xvf models.tgz; popd'