from MobileKG.GenerateKG.operation.FeatureExtract import FeatureExtract
from MobileKG.GenerateKG.operation.GenerateGraph import GenerateGraph
import os
from MobileKG.Config.RunConfig import *
from MobileKG.GenerateKG.operation.RelationExtract import RelationExtract


# data transformation
def analyze():
    print('Begin Transformation')
    original_path = original_data_path
    result_path = analyze_data_path
    trans = FeatureExtract(None, original_path, result_path)
    trans.execute()
    print('Transformation Complete')
    return


def connect():
    print('Begin Connection')
    root = analyze_data_path + '/'
    dirs = []
    apps = os.listdir(root)
    for app in apps:
        path = os.listdir(root + app)
        for p in path:
            dirs.append(root + app + '/' + p)
    # dirs=[root+'MaoYan/MaoYan-01']
    c = RelationExtract(dirs, ocr_similarity, opt_similarity, operation_input_similarity, connect_data_path, generate_supply_path)
    c.execute()
    print('Connection Complete')


def generate():
    print('Begin KG Generation')
    gen = GenerateGraph(generate_data_path)
    gen.execute()
    print('KG Generation Conplete')
    return


# analyze()
# connect()
generate()
