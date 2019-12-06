@echo off
set project_name=geotransform
set execpath=%cd%

:: Move script path to current
cd /d %~dp0
cd ../

@echo on
python -m %project_name% conf/config.json

@echo off
cd /d %execpath%
