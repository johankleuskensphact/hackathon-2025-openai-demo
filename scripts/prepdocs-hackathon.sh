 #!/bin/sh

. ./scripts/load_python_env.sh

echo 'Running "prepdocs.py"'

additionalArgs=""
if [ $# -gt 0 ]; then
  additionalArgs="$@"
fi

for dir in ./data/*/; do
  category=$(basename "$dir")
  echo "Processing directory: $dir"
  echo "Setting category: $category"
  ./.venv/bin/python ./app/backend/prepdocs.py "$dir" --category $category --verbose $additionalArgs
done
