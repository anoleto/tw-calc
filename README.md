python3.9 -m pip install -r requirements.txt
cd calc
maturin develop --release
cd ..
python3.9 main.py