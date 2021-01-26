@echo off

set pwd=%CD%
set pyrevit=%1
set extensions=%2
set log="C:\temp\pyRevitUpdate.log"

echo %DATE% >%log% 2>&1
echo %TIME% >>%log% 2>&1

call :pull %pyrevit% >>%log% 2>&1

cd "%extensions%"

for /D %%d in (*) do (
	if exist "%%d\.git" (
		call :pull %extensions%\%%d >>%log% 2>&1
	)
)

cd %pwd%

goto:end

:pull
echo:
cd %1
echo %1
set "status="
for /f "delims=" %%s in ('git status --porcelain') do set status=%%s
if not "%status%" == "" (
	echo Working copy is dirty - skipping
) else (
	git pull
)
cd ..

:end