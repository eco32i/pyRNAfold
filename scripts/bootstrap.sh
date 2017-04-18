#!/bin/bash -e 
tabs 4
clear
readonly VENV_DIR=$HOME/.venv
readonly ENV="pyRNA"

install_deps() {
    sudo add-apt-repository ppa:j-4/vienna-ppa -y
    sudo apt update
    sudo apt install -y 
        libcurl4-openssl-dev python-dev python3-dev build-essential git \
        libopenblas-base libopenblas-dev gfortran \
        g++ python-pip samtools bedtools libpng-dev libjpeg8-dev \
        libfreetype6-dev libxft-dev libatlas3-base libatlas-dev \
        python3-venv libxml2-dev libxslt-dev vienna-rna
    sudo update-alternatives --set libblas.so.3 /usr/lib/openblas-base/libblas.so.3
    sudo update-alternatives --set liblapack.so.3 /usr/lib/openblas-base/liblapack.so.3
}


setup_env() {
    local pydata="requirements.txt"
    
    if [ -d $VENV_DIR/$ENV ]
    then
        rm -rf $VENV_DIR/$ENV
    fi

    pyvenv $VENV_DIR/$ENV
    source $VENV_DIR/$ENV/bin/activate
    pip install -U pip
    cat $pydata | xargs -n 1 -L 1 pip install
    deactivate
}



show_help() {
    cat <<EOF
    usage: $0 options

    Bootstraps a new ubuntu GNOME install to upgrade to the latest GNOME version, 
    setup most common dev dependencies, python stack, google browser and plugin, 
    and i3 windows manager.

    OPTIONS:

    -h | --help     display this help text and exit
    -d | --deps     install development and computational dependencies
    -c | --conda    set up conda environment
    -e | --env      set up python 3 virtualenv 
    -a | --all      all of the above
EOF
}

readonly OPTS=`getopt -o adeh --long all,deps,env,help -n 'bootstrap.sh' -- "$@"`

if [ $? != 0 ] ; then echo "Failed to parse options." >&2; exit 1; fi
eval set -- "$OPTS"

while true
do
    case "$1" in
        -a|--all)
            install_deps
            setup_env
            shift
            ;;
        -d|--deps)
            install_deps
            shift
            ;;
        -e|--env)
            setup_env
            shift
            ;;
        -h|--help)
            show_help
            shift
            ;;
        * )
            break
            ;;
    esac
done

