import os
import re
import json
from glob import glob

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

def get_files_to_process(source_dir, include_pattern, exclude_pattern):
    # Generate list of files to process based on the include and exclude patterns
    files = glob(os.path.join(source_dir, include_pattern), recursive=True)
    # Exclude files that match the exclude pattern
    exclude_files = glob(os.path.join(source_dir, exclude_pattern), recursive=True)
    return [file for file in files if file not in exclude_files]

def replace_strings_in_file(file_path, replacements):
    with open(file_path, 'r') as file:
        content = file.read()

    # Apply replacements using regex (case-sensitive)
    for replacement in replacements:
        old_str = replacement['old_str']
        new_str = replacement['new_str']

        # Use re.sub to perform the regex replacement (case-sensitive by default)
        content = re.sub(old_str, new_str, content)

    return content

def process_files(config):
    source_dir = config["source_dir"]
    output_dir = config["output_dir"]
    file_patterns = config["file_patterns"]

    # Ensure output_dir exists
    os.makedirs(output_dir, exist_ok=True)

    for pattern in file_patterns:
        include_pattern = pattern["include"]
        exclude_pattern = pattern["exclude"]
        replacements = pattern["replacements"]

        files_to_process = get_files_to_process(source_dir, include_pattern, exclude_pattern)

        for file_path in files_to_process:
            # Perform string replacement on the file
            modified_content = replace_strings_in_file(file_path, replacements)

            # Determine the output file path
            relative_path = os.path.relpath(file_path, source_dir)
            output_file_path = os.path.join(output_dir, relative_path)

            # Ensure the output directory structure exists
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # Write the modified content to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(modified_content)

            print(f"Processed and saved: {output_file_path}")

def main():
    config = load_config('config.json')
    process_files(config)

if __name__ == '__main__':
    main()
