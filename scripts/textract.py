import json
import sys

import textractor as t

if __name__ == '__main__':
    source_file = sys.argv[1]

    textractor = t.Textractor(source_file)
    results = []

    image_paths = textractor.pdf_to_image()

    for path in image_paths:
        blocks = textractor.get_blocks(path)
        
        table_blocks, blocks_map = textractor.get_table_blocks(blocks)
        
        for index, table in enumerate(table_blocks):
            rows = textractor.get_rows_columns_map(table, blocks_map)
            results.append(rows)

    json.dump(results, sys.stdout, indent=4)
