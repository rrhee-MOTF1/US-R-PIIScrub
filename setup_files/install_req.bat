@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_PIIBlur
conda install --file C:\US-R-PIIScrub\setup_files\requirements.txt -y --force-reinstall
