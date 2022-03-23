while getopts a:e:tp flag
do
    case "${flag}" in
        a) type=${OPTARG};;
        e) path=${OPTARG};;
        p) dump="yes";;
        t) time="True";;
    esac
done
if [[ -z $path ]]; then
    echo "Wrong path";
    exit 1;
fi
if [[ $type == "glouton" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 glouton.py -f $path -t;
    else 
        python3 glouton.py -f $path
    fi
elif [[ $type == "progdyn" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 progdyn.py -f $path -t;
    else
        python3 progdyn.py -f $path
    fi
elif [[ $type == "tabou" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 tabou.py -f $path -t;
    else
        python3 tabou.py -f $path
    fi
fi
if [[ $dump == "yes" ]]; then
    echo "$(<./data/result.txt)"
fi