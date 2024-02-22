@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_PIIBlur
conda install -c conda-forge ultralytics -y --force-reinstall
conda deactivate