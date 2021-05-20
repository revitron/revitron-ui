set cwd=%~dp0
cd %cwd%
cd ../docs
call make html
cd %cwd%