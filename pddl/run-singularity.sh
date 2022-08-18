set -euo pipefail

if [[ $# != 3 ]]; then
    echo "usage: $(basename "$0") image domain_file problem_file" 1>&2
    exit 2
fi

if [ -f output_plan ]; then
    echo "Error: remove output_plan" 1>&2
    exit 2
fi

# Ensure that strings like "CPU time limit exceeded" and "Killed" are in English.
export LANG=C

set +e
singularity run "$1" "$2" "$3"
set -e

# printf "\nRun VAL\n\n"

# for f in $PWD/output_plan*; do
#     validate -v "$PWD/$2" "$PWD/$3" "$f"
# done

