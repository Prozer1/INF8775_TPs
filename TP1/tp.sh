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
if [[ $type == "brute" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 brute_force_lent.py -f $path -t $time;
    else 
        python3 brute_force_lent.py -f $path -t "False"
    fi
elif [[ $type == "recursif" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 Diviser.py -f $path -t $time;
    else
        python3 Diviser.py -f $path -t "False"
    fi
elif [[ $type == "seuil" ]] ; then
    if [[ $time == "True" ]] ; then
        python3 diviser_seuil.py -f $path -t $time;
    else
        python3 diviser_seuil.py -f $path -t "False"
    fi
fi
if [[ $dump == "yes" ]]; then
    echo "$(<./data/result.txt)"
fi