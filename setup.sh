pythonexe=$(which python)
echo 'Found Python:   ' $pythonexe

pythonversion=$(python --version)
echo 'Python version: ' $pythonversion

sniperexe=$(which sniper.exe)
echo 'Found SNiPER:   ' $sniperexe

current_path=$(
             cd $(dirname "${BASH_SOURCE[0]}") 
             cd ..
             pwd
             )
echo 'Set Daisy path to PYTHONPATH: ' $current_path
export PYTHONPATH=$current_path:$PYTHONPATH

