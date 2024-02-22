@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_PIIBlur
conda install -c pytorch -c nvidia pytorch torchvision torchaudio pytorch-cuda=11.8 -y --force-reinstall
conda deactivate