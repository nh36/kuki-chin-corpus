#!/bin/bash
# Extract all Bible zip files to bibles/extracted/

cd "$(dirname "$0")/.."

for zip in *.zip; do
    # Extract ISO code from filename (e.g., "Tedim ctd-x-bible.zip" -> "ctd")
    iso=$(echo "$zip" | grep -oE '[a-z]{3}-x-bible' | cut -d'-' -f1)
    
    if [ -z "$iso" ]; then
        echo "Warning: Could not extract ISO from $zip, skipping"
        continue
    fi
    
    outdir="bibles/extracted/$iso"
    mkdir -p "$outdir"
    
    echo "Extracting $zip -> $outdir/"
    unzip -o -q "$zip" -d "$outdir"
done

echo "Done. Extracted files:"
ls -la bibles/extracted/
