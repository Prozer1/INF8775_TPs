while getopts e:p flag
do
    case "${flag}" in
        e) path=${OPTARG};;
        p) param="True";;
    esac
done
if [[ -z $path ]]; then
    echo "Wrong path";
    exit 1;
fi
if [[ $param == "True" ]] ; then
    python3 main.py -f $path -p True;
else 
    python3 main.py -f $path
fi