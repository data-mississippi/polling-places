import pathlib
import boto3
from pdf2image import convert_from_path

class Textractor:
    def __init__(self, source_file):
        self.source_file = source_file
    
    def get_intermediate_path(self):
        file_name = pathlib.Path(self.source_file).stem
        return f'intermediate/{file_name}'

    def convert_pdf_to_image(self):
        return convert_from_path(self.source_file, dpi=300, grayscale=True)
        
    def pdf_to_image(self):
        """Creates images from a PDF and returns the file paths."""
        images = self.convert_pdf_to_image()

        file_paths = []

        for index, image in enumerate(images):
            path = f'{self.get_intermediate_path()}_{index}.jpg'
            image.save(path, 'JPEG')
            file_paths.append(path)

        return file_paths
    
    def get_blocks(self, path):
        """
        Returns AWS Textract blocks for forms.
        """
        with open(path, 'rb') as file:
            img_test = file.read()
            bytes_test = bytearray(img_test)

        client = boto3.client('textract')
        response = client.analyze_document(
            Document={'Bytes': bytes_test},
            FeatureTypes=['TABLES']
        )

        return response['Blocks']
    
    def get_table_blocks(self, blocks):
        table_blocks = []
        blocks_map = {}
        
        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)
                
        return table_blocks, blocks_map
    
    def get_rows_columns_map(self, table_result, blocks_map):
        rows = {}
        for relationship in table_result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}
                            
                        # get the text value
                        rows[row_index][col_index] = self.get_text(cell, blocks_map)
        return rows

    def get_kv_map(self, blocks):
        key_map = {}
        value_map = {}
        block_map = {}
        for block in blocks:
            block_id = block['Id']
            block_map[block_id] = block
            if block['BlockType'] == "KEY_VALUE_SET":
                if 'KEY' in block['EntityTypes']:
                    key_map[block_id] = block
                else:
                    value_map[block_id] = block

        return key_map, value_map, block_map

    def find_value_block(self, key_block, value_map):
        for relationship in key_block['Relationships']:
            if relationship['Type'] == 'VALUE':
                for value_id in relationship['Ids']:
                    value_block = value_map[value_id]
        return value_block

    def get_text(self, result, blocks_map):
        text = ''
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] =='SELECTED':
                                text +=  'X '    
        return text
    
    def get_kv_relationship(self, key_map, value_map, block_map):
        kvs = {}
        for block_id, key_block in key_map.items():
            value_block = self.find_value_block(key_block, value_map)
            key = self.get_text(key_block, block_map).strip().replace(':', '')
            val = self.get_text(value_block, block_map).strip()
            kvs[key] = val
        return kvs


# import boto3

# class Textractor:
#     def get_blocks(self, path):
#         """
#         Returns AWS Textract blocks for forms.
#         """
#         with open(path, 'rb') as file:
#             img_test = file.read()
#             bytes_test = bytearray(img_test)

#         client = boto3.client('textract')
#         response = client.analyze_document(
#             Document={'Bytes': bytes_test},
#             FeatureTypes=['FORMS']
#         )

#         return response['Blocks']

#     def get_kv_map(self, blocks):
#         key_map = {}
#         value_map = {}
#         block_map = {}
#         for block in blocks:
#             block_id = block['Id']
#             block_map[block_id] = block
#             if block['BlockType'] == "KEY_VALUE_SET":
#                 if 'KEY' in block['EntityTypes']:
#                     key_map[block_id] = block
#                 else:
#                     value_map[block_id] = block

#         return key_map, value_map, block_map

#     def find_value_block(self, key_block, value_map):
#         for relationship in key_block['Relationships']:
#             if relationship['Type'] == 'VALUE':
#                 for value_id in relationship['Ids']:
#                     value_block = value_map[value_id]
#         return value_block

#     def get_text(self, result, blocks_map):
#         text = ''
#         if 'Relationships' in result:
#             for relationship in result['Relationships']:
#                 if relationship['Type'] == 'CHILD':
#                     for child_id in relationship['Ids']:
#                         word = blocks_map[child_id]
#                         if word['BlockType'] == 'WORD':
#                             text += word['Text'] + ' '
#                         if word['BlockType'] == 'SELECTION_ELEMENT':
#                             if word['SelectionStatus'] == 'SELECTED':
#                                 text += 'X '    
    
#         return text
    
#     def get_kv_relationship(self, key_map, value_map, block_map):
#         kvs = {}
#         for block_id, key_block in key_map.items():
#             value_block = self.find_value_block(key_block, value_map)
#             key = self.get_text(key_block, block_map).strip().replace(':', '')
#             val = self.get_text(value_block, block_map).strip()
#             kvs[key] = val
#         return kvs
