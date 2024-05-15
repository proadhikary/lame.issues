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
pip3 install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

## Git Hacks
Get inside your specific folder
```
cd FolderName
```
Initialize .git
```
git init
```
Add all the files
```
git add .
```
Checkt he status if all the added or not
```
git status
```
Commit with message
```
git commit -m "details"
```
Run this to change brunch
```
git checkout -b main
```
Add origin
```
git remote add origin "url"
```
Push
```
git push --set-upstream origin main
```
