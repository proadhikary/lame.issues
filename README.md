# Lame Issues


## IITD Proxy in Jupyter
```
import os
os.environ['http_proxy']="http://xen03.iitd.ac.in:3128"
os.environ['https_proxy']="http://xen03.iitd.ac.in:3128"
```

## IIID Proxy for Terminal
```
import os
export http_proxy="http://xen03.iitd.ac.in:3128"
export https_proxy="http://xen03.iitd.ac.in:3128"
```

## Install pytorch version 2.0.1
```
python -m pip install torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
