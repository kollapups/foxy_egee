# convert_encoding.py
with open('foxy_ege_scopy.sql', 'r', encoding='utf-16le') as input_file:
    content = input_file.read()
with open('foxy_ege_scopy_utf8.sql', 'w', encoding='utf-8') as output_file:
    output_file.write(content)