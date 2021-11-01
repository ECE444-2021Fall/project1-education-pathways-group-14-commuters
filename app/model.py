import pandas as pd
import pickle
import networkx as nx

import os
working_dir = os.getcwd()


with open(working_dir+'/app'+'/resources/course_vectorizer.pickle','rb') as f:
    vectorizer = pickle.load(f)
with open(working_dir+'/app'+'/resources/course_vectors.npz','rb') as f:
    course_vectors = pickle.load(f)
with open(working_dir+'/app'+'/resources/graph.pickle','rb') as f:
    G = nx.read_gpickle(f)
df = pd.read_pickle(working_dir+'/app'+'/resources/df_processed.pickle').set_index('Code')