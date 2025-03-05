filepath: /mnt/e/ProgrammingWorkspaces/Uzabase/code/script/run.sh
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CFG_FILE="$DIR/../config/config.yaml"
OUTPUT_DIR="$DIR/../../ztmp/data"
mkdir -p "$OUTPUT_DIR"

echo "Running specific words count..."
python3 "$DIR/../src/main.py" process_data --cfg "$CFG_FILE" -dataset news --dirout "$OUTPUT_DIR"

echo "Running all words count..."
python3 "$DIR/../src/main.py" process_data_all --cfg "$CFG_FILE" -dataset news --dirout "$OUTPUT_DIR"
