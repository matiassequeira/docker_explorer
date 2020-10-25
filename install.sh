pip3 install -r requirements.txt
chmod +x ExploreAll ExploreImage
export PATH=$(pwd):$PATH
cd ../
git clone https://github.com/matiassequeira/whispers_mod
cd whispers_mod
make install