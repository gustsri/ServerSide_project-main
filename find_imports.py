import ast
import os

def get_imports(directory):
    imports = set()
    for root, dirs, files in os.walk(directory):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module.split('.')[0])
                except Exception as e:
                    pass
    return imports

if __name__ == "__main__":
    directory = r"d:\Gus\Old-accont-git\ServerSide_project-main\my_project\myshop"
    all_imports = get_imports(directory)
    print("ALL IMPORTS:")
    for imp in sorted(all_imports):
        print(imp)
