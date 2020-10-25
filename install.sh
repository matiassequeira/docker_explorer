pip3 install -r requirements.txt
chmod +x ExploreAll ExploreImage install.sh cleanup.sh utils/TriageBlockerAndCritical.py
export PATH=$(pwd):$PATH
cd ../ && git clone https://github.com/matiassequeira/whispers
cd whispers && make install