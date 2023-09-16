import re


def remove_comments(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        code = infile.read()
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        # Remove single-line comments
        code = re.sub(r'//.*', '', code)
        outfile.write(code)
