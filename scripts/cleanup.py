import os
import json

def recurse_dir(path:str="") -> list[str]:
    to_return = []
    if os.path.isfile(path=path):
        if '.DS_Store' not in path:
            to_return.append(path)
    else:
        for dir in os.listdir(path=path):
            to_return += recurse_dir(path=f"{path}/{dir}")
    return to_return

def remove_asset_receipt(asset:dict={}):
    if '_AssetReceipt' in asset:
        del asset['_AssetReceipt']

def write_to_file(file_path:str, data:dict):
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, indent=4, separators=(',',':')))

def read_from_file(file_path:str) -> dict:
    with open(file_path, 'r') as f:
        temp = json.loads(f.read())
    return temp

def remove_receipt_from_paths(paths:list[str]):
    for dir in paths:
        d = read_from_file(dir)
        if 'Assets' in d:
            for asset in d['Assets']:
                remove_asset_receipt(asset=asset)
        write_to_file(file_path=dir, data=d)

if __name__ == "__main__":
    start_dir = "/Users/riigess/Documents/Github/UAFAssets/raw/"
    dirs = recurse_dir(start_dir)
    remove_receipt_from_paths(dirs)
