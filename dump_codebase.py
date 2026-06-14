import os

def dump_codebase(root_dir, output_file, extensions=('.py', '.css', '.html', '.md')):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude common ignore directories
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('__pycache__', 'venv', 'env', 'node_modules')]
            
            for filename in filenames:
                if filename.endswith(extensions):
                    filepath = os.path.join(dirpath, filename)
                    outfile.write("="*80 + "\n")
                    outfile.write(f"FILE: {os.path.relpath(filepath, root_dir)}\n")
                    outfile.write("="*80 + "\n")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}\n")
                    outfile.write("\n\n")

if __name__ == "__main__":
    root_dir = "."
    output_file = "codebase_dump.txt"
    dump_codebase(root_dir, output_file)
    print(f"Codebase dumped to {output_file}")
