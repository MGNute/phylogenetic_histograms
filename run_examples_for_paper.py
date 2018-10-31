import os.path
from art_manager import ArtManager
from data_controller import SeppJsonDataManager
from phylohist import *

base_folder = os.path.split(os.path.abspath(__file__))[0]
test_folder = os.path.join(base_folder,'test')

am = ArtManager()
dc = SeppJsonDataManager()
annot_file = os.path.join(test_folder,'ref_tree_annotation.txt')


