@echo off

if "%1" == "test" (
	vagrant up && vagrant ssh --command "temp=$(mktemp --directory) && rsync --recurisve --exclude='.*' /vagrant/* $temp && cd $temp && chmod 644 test/*.py && nosetests"
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "clean" (
	vagrant destroy --force
	if errorlevel 1 exit /b 1
	goto end
)

:end
