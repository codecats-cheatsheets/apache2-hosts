#!/bin/bash
#save script name it p.sh, next chmod 755 ~/p.sh
#run script by command: `. p.sh my_project`

#find virtual enviroment and activate it. Virtual enviroments is in predefined array but 
#script will add extra root of predefined directory (/some/path/ => /some/../path/)
find_venv() {
	local -n envs_passed=$1
	local envs=()
	local directory=$2
	local activated=false
	for env in ${envs_passed[*]}
	do
		envs+=($directory/$env)
		envs+=($directory/../$env)
	done

	for env in ${envs[*]}
	do
		local env_activate=$env/bin/activate
                #If found virtual env just activate it
		if [ -f $env_activate ]; then
			echo 'Found virtualenv in ' $env_activate
			activate_venv $env_activate
			activated=true
			echo 'Activated'
			break
		fi
	done
	if [ -z $activated ]; then
		echo 'Not found virtualenv in ' ${envs[*]}
	fi
}
activate_venv() {
	source $1
}
#run django server if manage.py exists in found directory
runserver() {
	if [ -f $1/manage.py ]; then
		$1/manage.py runserver
	else
		echo 'No server to start at ' $1
	fi
}
#predefined working dirs
directories=("django" "other" "bottle")
dirs=()
#project name passed to script
project=''
#project can has subdirectory (in this case always hardcoded src)
project_subdir='src'
#predefined virtual enviroments directories names
venv=("venv" "env")

#get project name
if [ ! -z "$1" ]; then
	project=$1
fi
#get virtual enviroment name (not required)
if [ ! -z "$3" ]; then
	venv=($3)
fi
#add extra project subdirectory
for item in ${directories[*]}
do
	dirs+=($item/$project/$project_subdir $item/$project)
done

#find project in dirs
for item in ${dirs[*]}
do
	directory=~/py/$item
        #found project
	if [ -d $directory ]; then
		find_venv venv $directory	
		echo $directory
		#run server if 2nd argument is true
		case "$2" in
			0|f|false|False|FALSE*)
        			echo 'Server offline'
        		;;
			1|t|true|True|TRUE*)
        			runserver $directory
        		;;
		esac
		cd $directory
		break
	fi
done 
