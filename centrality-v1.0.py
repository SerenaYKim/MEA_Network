# -*- coding: utf-8 -*-
"""Renewable-Diffusion-Network-Centrality.ipynb

Automatically generated by Colaboratory.

Original file is located at

"""

gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Select the Runtime > "Change runtime type" menu to enable a GPU accelerator, ')
  print('and then re-execute this cell.')
else:
  print(gpu_info)

from psutil import virtual_memory
ram_gb = virtual_memory().total / 1e9
print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

if ram_gb < 20:
  print('To enable a high-RAM runtime, select the Runtime > "Change runtime type"')
  print('menu, and then select High-RAM in the Runtime shape dropdown. Then, ')
  print('re-execute this cell.')
else:
  print('You are using a high-RAM runtime!')

import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import itertools as iter
from random import sample
from itertools import chain 
import csv
import glob
import os
import pickle
import scipy
from scipy import stats
from functools import reduce
import operator
from numpy.random import randint
import matplotlib

from graph_tool.all import *
import graph_tool.all as gt


# https://graph-tool.skewed.de/static/doc/draw.html?highlight=vertex%20list 
# https://graph-tool.skewed.de/static/doc/quickstart.html

# Load Edge Data and ISO Code
mea = pd.read_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataMEA_Ctrlity/MEA_v1.1_2000_2020_toMerge.csv') #all MEAs from 2000 to 2020
iso = pd.read_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataMEA_Ctrlity/MEA_v1.2_MEA_ISO_crosswalk.csv') #iso country code

# Merging data 
frame = [mea, iso]
mea_iso_merged = reduce(lambda left,right: pd.merge(left, right, on=['Country'],
                                            how='inner'), frame).fillna('0')

# Exporting data

#mea_iso_merged.to_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataMEA_Ctrlity/MEA_ISO_Merged.csv')

# MEA_2000-2008
mea_2000_2008 = mea_iso_merged[mea_iso_merged["Year"] < 2009]

# MEA_2003-2011
mea_2003_2011 = mea_iso_merged[2002 < mea_iso_merged["Year"]]
mea_2003_2011 = mea_2003_2011[mea_2003_2011["Year"] < 2012]

# MEA 2005-2013
mea_2005_2013 = mea_iso_merged[2004 < mea_iso_merged["Year"]]
mea_2005_2013 = mea_2005_2013[mea_2005_2013["Year"] < 2014]

# MEA 2007-2015
mea_2007_2015 = mea_iso_merged[2006 < mea_iso_merged["Year"]]
mea_2007_2015 = mea_2007_2015[mea_2007_2015["Year"] < 2016]

# MEA 2010-2018
mea_2010_2018 = mea_iso_merged[2009 < mea_iso_merged["Year"]]
mea_2010_2018 = mea_2010_2018[mea_2010_2018["Year"] < 2019]

# Generate Graphs 
G_2000_2008 = nx.convert_matrix.from_pandas_edgelist(mea_2000_2008, source='Ctry_Code', target='iea')
G_2003_2011 = nx.convert_matrix.from_pandas_edgelist(mea_2003_2011, source='Ctry_Code', target='iea')
G_2005_2013 = nx.convert_matrix.from_pandas_edgelist(mea_2005_2013, source='Ctry_Code', target='iea')
G_2007_2015 = nx.convert_matrix.from_pandas_edgelist(mea_2007_2015, source='Ctry_Code', target='iea')
G_2010_2018 = nx.convert_matrix.from_pandas_edgelist(mea_2010_2018, source='Ctry_Code', target='iea')

# Vertex data
vertex = pd.read_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataMEA_Ctrlity/mea_vertex_final_5352.csv')
node_attr = vertex.set_index('node').to_dict('index') #https://stackoverflow.com/questions/54497929/networkx-setting-node-attributes-from-dataframe/54662176 

# Bipartite classification attached to each graph 
nx.set_node_attributes(G_2000_2008, node_attr)
nx.set_node_attributes(G_2003_2011, node_attr)
nx.set_node_attributes(G_2005_2013, node_attr)
nx.set_node_attributes(G_2007_2015, node_attr)
nx.set_node_attributes(G_2010_2018, node_attr)

# One-mode projection of countries 

# 2000_2008 for 2009 data
top_nodes = {n for n, d in G_2000_2008.nodes(data=True) if G_2000_2008.nodes[n]['bipartite'] == 1}
bottom_nodes = {n for n, d in G_2000_2008.nodes(data=True) if G_2000_2008.nodes[n]['bipartite'] == 0}
C_2000_2008 = bipartite.projected_graph(G_2000_2008, top_nodes)

# 2003-2011 for 2012 data
top_nodes = {n for n, d in G_2003_2011.nodes(data=True) if G_2003_2011.nodes[n]['bipartite'] == 1}
bottom_nodes = {n for n, d in G_2003_2011.nodes(data=True) if G_2003_2011.nodes[n]['bipartite'] == 0}
C_2003_2011 = bipartite.projected_graph(G_2003_2011, top_nodes)

# 2005-2013 for 2014 data
top_nodes = {n for n, d in G_2005_2013.nodes(data=True) if G_2005_2013.nodes[n]['bipartite'] == 1}
bottom_nodes = {n for n, d in G_2005_2013.nodes(data=True) if G_2005_2013.nodes[n]['bipartite'] == 0}
C_2005_2013 = bipartite.projected_graph(G_2005_2013, top_nodes)

# 2007-2015 for 2016 data
top_nodes = {n for n, d in G_2007_2015.nodes(data=True) if G_2007_2015.nodes[n]['bipartite'] == 1}
bottom_nodes = {n for n, d in G_2007_2015.nodes(data=True) if G_2007_2015.nodes[n]['bipartite'] == 0}
C_2007_2015 = bipartite.projected_graph(G_2007_2015, top_nodes)

# 2010-2018 for 2019 data
top_nodes = {n for n, d in G_2010_2018.nodes(data=True) if G_2010_2018.nodes[n]['bipartite'] == 1}
bottom_nodes = {n for n, d in G_2010_2018.nodes(data=True) if G_2010_2018.nodes[n]['bipartite'] == 0}
C_2010_2018 = bipartite.projected_graph(G_2010_2018, top_nodes)

# Create separate graphs for each centrality measure (for future use)

C_2000_2008_eigenvec = C_2000_2008
C_2000_2008_harmnic = C_2000_2008
C_2000_2008_btwness = C_2000_2008
C_2000_2008_sprding = C_2000_2008

C_2003_2011_eigenvec = C_2003_2011
C_2003_2011_harmnic = C_2003_2011
C_2003_2011_btwness = C_2003_2011
C_2003_2011_sprding = C_2003_2011

C_2005_2013_eigenvec = C_2005_2013
C_2005_2013_harmnic = C_2005_2013
C_2005_2013_btwness = C_2005_2013
C_2005_2013_sprding = C_2005_2013

C_2007_2015_eigenvec = C_2007_2015
C_2007_2015_harmnic = C_2007_2015
C_2007_2015_btwness = C_2007_2015
C_2007_2015_sprding = C_2007_2015

C_2010_2018_eigenvec = C_2010_2018
C_2010_2018_harmnic = C_2010_2018
C_2010_2018_btwness = C_2010_2018
C_2010_2018_sprding = C_2010_2018

# graph-tool conversions 
C_2010_2018_gt = C_2010_2018
nx.write_graphml_lxml(C_2010_2018_gt, "mea_2018_gt.graphml")
gt_2018_univ = graph_tool.load_graph("mea_2018_gt.graphml", fmt='auto', ignore_vp=None, ignore_ep=None, ignore_gp=None)

# extra
C_2010_2018_eigenvec_gt = C_2010_2018
C_2010_2018_harmnic_gt = C_2010_2018

# Eigenvector centrality graph-tool 
nx.write_graphml_lxml(C_2010_2018_eigenvec_gt, "mea_eigen_ctrlty_2018_gt.graphml")
gt_eigen_2018_new = graph_tool.load_graph("mea_eigen_ctrlty_2018_gt.graphml", fmt='auto', ignore_vp=None, ignore_ep=None, ignore_gp=None)

# harmonic centrality graph-tool 
nx.write_graphml_lxml(C_2010_2018_harmnic_gt, "mea_harmnic_ctrlty_2018_gt.graphml")
gt_harmnic_2018_new = graph_tool.load_graph("mea_harmnic_ctrlty_2018_gt.graphml", fmt='auto', ignore_vp=None, ignore_ep=None, ignore_gp=None)

# Eigenvector centrality

eigen_cent_2000_2008 = nx.algorithms.centrality.eigenvector_centrality(C_2000_2008)
eigen_cent_2003_2011 = nx.algorithms.centrality.eigenvector_centrality(C_2003_2011)
eigen_cent_2005_2013 = nx.algorithms.centrality.eigenvector_centrality(C_2005_2013)
eigen_cent_2007_2015 = nx.algorithms.centrality.eigenvector_centrality(C_2007_2015)
eigen_cent_2010_2018 = nx.algorithms.centrality.eigenvector_centrality(C_2010_2018)

sorted_eigen_2000_2008 = dict(sorted(eigen_cent_2000_2008.items(), key=operator.itemgetter(1),reverse=True))
sorted_eigen_2003_2011 = dict(sorted(eigen_cent_2003_2011.items(), key=operator.itemgetter(1),reverse=True))
sorted_eigen_2005_2013 = dict(sorted(eigen_cent_2005_2013.items(), key=operator.itemgetter(1),reverse=True))
sorted_eigen_2007_2015 = dict(sorted(eigen_cent_2007_2015.items(), key=operator.itemgetter(1),reverse=True))
sorted_eigen_2010_2018 = dict(sorted(eigen_cent_2010_2018.items(), key=operator.itemgetter(1),reverse=True))
#list_eigen = [(k, v) for k, v in sorted_eigen.items()] 
#list_eigen

df_eigen_2008 = pd.DataFrame(list(sorted_eigen_2000_2008.items()),columns = ['ctry','eigenvector_centrality'])
df_eigen_2011 = pd.DataFrame(list(sorted_eigen_2003_2011.items()),columns = ['ctry','eigenvector_centrality'])
df_eigen_2013 = pd.DataFrame(list(sorted_eigen_2005_2013.items()),columns = ['ctry','eigenvector_centrality'])
df_eigen_2015 = pd.DataFrame(list(sorted_eigen_2007_2015.items()),columns = ['ctry','eigenvector_centrality'])
df_eigen_2018 = pd.DataFrame(list(sorted_eigen_2010_2018.items()),columns = ['ctry','eigenvector_centrality'])

df_eigen_2008['eigenvector_centrality'] = df_eigen_2008['eigenvector_centrality']*10
df_eigen_2011['eigenvector_centrality'] = df_eigen_2011['eigenvector_centrality']*10
df_eigen_2013['eigenvector_centrality'] = df_eigen_2013['eigenvector_centrality']*10
df_eigen_2015['eigenvector_centrality'] = df_eigen_2015['eigenvector_centrality']*10
df_eigen_2018['eigenvector_centrality'] = df_eigen_2018['eigenvector_centrality']*10

df_eigen_2008['stad_eigenvector'] = (df_eigen_2008['eigenvector_centrality'] - df_eigen_2008['eigenvector_centrality'].mean())/df_eigen_2008['eigenvector_centrality'].std()
df_eigen_2011['stad_eigenvector'] = (df_eigen_2011['eigenvector_centrality'] - df_eigen_2011['eigenvector_centrality'].mean())/df_eigen_2011['eigenvector_centrality'].std()
df_eigen_2013['stad_eigenvector'] = (df_eigen_2013['eigenvector_centrality'] - df_eigen_2013['eigenvector_centrality'].mean())/df_eigen_2013['eigenvector_centrality'].std()
df_eigen_2015['stad_eigenvector'] = (df_eigen_2015['eigenvector_centrality'] - df_eigen_2015['eigenvector_centrality'].mean())/df_eigen_2015['eigenvector_centrality'].std()
df_eigen_2018['stad_eigenvector'] = (df_eigen_2018['eigenvector_centrality'] - df_eigen_2018['eigenvector_centrality'].mean())/df_eigen_2018['eigenvector_centrality'].std()

df_eigen_2008['year'] = 2009 
df_eigen_2011['year'] = 2012
df_eigen_2013['year'] = 2014
df_eigen_2015['year'] = 2016
df_eigen_2018['year'] = 2019

# Harmonic centrality

harmnic_cent_2000_2008 = nx.algorithms.centrality.harmonic_centrality(C_2000_2008)
harmnic_cent_2003_2011 = nx.algorithms.centrality.harmonic_centrality(C_2003_2011)
harmnic_cent_2005_2013 = nx.algorithms.centrality.harmonic_centrality(C_2005_2013)
harmnic_cent_2007_2015 = nx.algorithms.centrality.harmonic_centrality(C_2007_2015)
harmnic_cent_2010_2018 = nx.algorithms.centrality.harmonic_centrality(C_2010_2018)

sorted_harmnic_2000_2008 = dict(sorted(harmnic_cent_2000_2008.items(), key=operator.itemgetter(1),reverse=True))
sorted_harmnic_2003_2011 = dict(sorted(harmnic_cent_2003_2011.items(), key=operator.itemgetter(1),reverse=True))
sorted_harmnic_2005_2013 = dict(sorted(harmnic_cent_2005_2013.items(), key=operator.itemgetter(1),reverse=True))
sorted_harmnic_2007_2015 = dict(sorted(harmnic_cent_2007_2015.items(), key=operator.itemgetter(1),reverse=True))
sorted_harmnic_2010_2018 = dict(sorted(harmnic_cent_2010_2018.items(), key=operator.itemgetter(1),reverse=True))
#list_harmnic = [(k, v) for k, v in sorted_harmnic.items()] 
#list_harmnic

df_harmnic_2008 = pd.DataFrame(list(sorted_harmnic_2000_2008.items()),columns = ['ctry','harmonic_centrality'])
df_harmnic_2011 = pd.DataFrame(list(sorted_harmnic_2003_2011.items()),columns = ['ctry','harmonic_centrality'])
df_harmnic_2013 = pd.DataFrame(list(sorted_harmnic_2005_2013.items()),columns = ['ctry','harmonic_centrality'])
df_harmnic_2015 = pd.DataFrame(list(sorted_harmnic_2007_2015.items()),columns = ['ctry','harmonic_centrality'])
df_harmnic_2018 = pd.DataFrame(list(sorted_harmnic_2010_2018.items()),columns = ['ctry','harmonic_centrality'])

#df_harmnic_2008['harmonic_centrality'] = df_harmnic_2008['harmonic_centrality']*10
#df_harmnic_2011['harmonic_centrality'] = df_harmnic_2011['harmonic_centrality']*10
#df_harmnic_2013['harmonic_centrality'] = df_harmnic_2013['harmonic_centrality']*10
#df_harmnic_2015['harmonic_centrality'] = df_harmnic_2015['harmonic_centrality']*10
#df_harmnic_2018['harmonic_centrality'] = df_harmnic_2018['harmonic_centrality']*10

df_harmnic_2008['stad_harmonic'] = (df_harmnic_2008['harmonic_centrality'] - df_harmnic_2008['harmonic_centrality'].mean())/df_harmnic_2008['harmonic_centrality'].std()
df_harmnic_2011['stad_harmonic'] = (df_harmnic_2011['harmonic_centrality'] - df_harmnic_2011['harmonic_centrality'].mean())/df_harmnic_2011['harmonic_centrality'].std()
df_harmnic_2013['stad_harmonic'] = (df_harmnic_2013['harmonic_centrality'] - df_harmnic_2013['harmonic_centrality'].mean())/df_harmnic_2013['harmonic_centrality'].std()
df_harmnic_2015['stad_harmonic'] = (df_harmnic_2015['harmonic_centrality'] - df_harmnic_2015['harmonic_centrality'].mean())/df_harmnic_2015['harmonic_centrality'].std()
df_harmnic_2018['stad_harmonic'] = (df_harmnic_2018['harmonic_centrality'] - df_harmnic_2018['harmonic_centrality'].mean())/df_harmnic_2018['harmonic_centrality'].std()

df_harmnic_2008['year'] = 2009 
df_harmnic_2011['year'] = 2012
df_harmnic_2013['year'] = 2014
df_harmnic_2015['year'] = 2016
df_harmnic_2018['year'] = 2019

# Betweenness centrality

betweenness_cent_2000_2008 = nx.algorithms.centrality.betweenness_centrality(C_2000_2008)
betweenness_cent_2003_2011 = nx.algorithms.centrality.betweenness_centrality(C_2003_2011)
betweenness_cent_2005_2013 = nx.algorithms.centrality.betweenness_centrality(C_2005_2013)
betweenness_cent_2007_2015 = nx.algorithms.centrality.betweenness_centrality(C_2007_2015)
betweenness_cent_2010_2018 = nx.algorithms.centrality.betweenness_centrality(C_2010_2018)

sorted_betweenness_2000_2008 = dict(sorted(betweenness_cent_2000_2008.items(), key=operator.itemgetter(1),reverse=True))
sorted_betweenness_2003_2011 = dict(sorted(betweenness_cent_2003_2011.items(), key=operator.itemgetter(1),reverse=True))
sorted_betweenness_2005_2013 = dict(sorted(betweenness_cent_2005_2013.items(), key=operator.itemgetter(1),reverse=True))
sorted_betweenness_2007_2015 = dict(sorted(betweenness_cent_2007_2015.items(), key=operator.itemgetter(1),reverse=True))
sorted_betweenness_2010_2018 = dict(sorted(betweenness_cent_2010_2018.items(), key=operator.itemgetter(1),reverse=True))
#list_betweenness = [(k, v) for k, v in sorted_betweenness.items()] 
#list_betweenness

df_betweenness_2008 = pd.DataFrame(list(sorted_betweenness_2000_2008.items()),columns = ['ctry','betweenness_centrality'])
df_betweenness_2011 = pd.DataFrame(list(sorted_betweenness_2003_2011.items()),columns = ['ctry','betweenness_centrality'])
df_betweenness_2013 = pd.DataFrame(list(sorted_betweenness_2005_2013.items()),columns = ['ctry','betweenness_centrality'])
df_betweenness_2015 = pd.DataFrame(list(sorted_betweenness_2007_2015.items()),columns = ['ctry','betweenness_centrality'])
df_betweenness_2018 = pd.DataFrame(list(sorted_betweenness_2010_2018.items()),columns = ['ctry','betweenness_centrality'])

#df_betweenness_2008['betweenness_centrality'] = df_betweenness_2008['betweenness_centrality']*10
#df_betweenness_2011['betweenness_centrality'] = df_betweenness_2011['betweenness_centrality']*10
#df_betweenness_2013['betweenness_centrality'] = df_betweenness_2013['betweenness_centrality']*10
#df_betweenness_2015['betweenness_centrality'] = df_betweenness_2015['betweenness_centrality']*10
#df_betweenness_2018['betweenness_centrality'] = df_betweenness_2018['betweenness_centrality']*10

df_betweenness_2008['stad_betweenness'] = (df_betweenness_2008['betweenness_centrality'] - df_betweenness_2008['betweenness_centrality'].mean())/df_betweenness_2008['betweenness_centrality'].std()
df_betweenness_2011['stad_betweenness'] = (df_betweenness_2011['betweenness_centrality'] - df_betweenness_2011['betweenness_centrality'].mean())/df_betweenness_2011['betweenness_centrality'].std()
df_betweenness_2013['stad_betweenness'] = (df_betweenness_2013['betweenness_centrality'] - df_betweenness_2013['betweenness_centrality'].mean())/df_betweenness_2013['betweenness_centrality'].std()
df_betweenness_2015['stad_betweenness'] = (df_betweenness_2015['betweenness_centrality'] - df_betweenness_2015['betweenness_centrality'].mean())/df_betweenness_2015['betweenness_centrality'].std()
df_betweenness_2018['stad_betweenness'] = (df_betweenness_2018['betweenness_centrality'] - df_betweenness_2018['betweenness_centrality'].mean())/df_betweenness_2018['betweenness_centrality'].std()

df_betweenness_2008['year'] = 2009 
df_betweenness_2011['year'] = 2012
df_betweenness_2013['year'] = 2014
df_betweenness_2015['year'] = 2016
df_betweenness_2018['year'] = 2019

# Degree centrality

degree_cent_2000_2008 = nx.algorithms.centrality.degree_centrality(C_2000_2008)
degree_cent_2003_2011 = nx.algorithms.centrality.degree_centrality(C_2003_2011)
degree_cent_2005_2013 = nx.algorithms.centrality.degree_centrality(C_2005_2013)
degree_cent_2007_2015 = nx.algorithms.centrality.degree_centrality(C_2007_2015)
degree_cent_2010_2018 = nx.algorithms.centrality.degree_centrality(C_2010_2018)

sorted_degree_2000_2008 = dict(sorted(degree_cent_2000_2008.items(), key=operator.itemgetter(1),reverse=True))
sorted_degree_2003_2011 = dict(sorted(degree_cent_2003_2011.items(), key=operator.itemgetter(1),reverse=True))
sorted_degree_2005_2013 = dict(sorted(degree_cent_2005_2013.items(), key=operator.itemgetter(1),reverse=True))
sorted_degree_2007_2015 = dict(sorted(degree_cent_2007_2015.items(), key=operator.itemgetter(1),reverse=True))
sorted_degree_2010_2018 = dict(sorted(degree_cent_2010_2018.items(), key=operator.itemgetter(1),reverse=True))
#list_degree = [(k, v) for k, v in sorted_degree.items()] 
#list_degree

df_degree_2008 = pd.DataFrame(list(sorted_degree_2000_2008.items()),columns = ['ctry','degree_centrality'])
df_degree_2011 = pd.DataFrame(list(sorted_degree_2003_2011.items()),columns = ['ctry','degree_centrality'])
df_degree_2013 = pd.DataFrame(list(sorted_degree_2005_2013.items()),columns = ['ctry','degree_centrality'])
df_degree_2015 = pd.DataFrame(list(sorted_degree_2007_2015.items()),columns = ['ctry','degree_centrality'])
df_degree_2018 = pd.DataFrame(list(sorted_degree_2010_2018.items()),columns = ['ctry','degree_centrality'])

#df_degree_2008['degree_centrality'] = df_degree_2008['degree_centrality']*10
#df_degree_2011['degree_centrality'] = df_degree_2011['degree_centrality']*10
#df_degree_2013['degree_centrality'] = df_degree_2013['degree_centrality']*10
#df_degree_2015['degree_centrality'] = df_degree_2015['degree_centrality']*10
#df_degree_2018['degree_centrality'] = df_degree_2018['degree_centrality']*10

df_degree_2008['stad_degree'] = (df_degree_2008['degree_centrality'] - df_degree_2008['degree_centrality'].mean())/df_degree_2008['degree_centrality'].std()
df_degree_2011['stad_degree'] = (df_degree_2011['degree_centrality'] - df_degree_2011['degree_centrality'].mean())/df_degree_2011['degree_centrality'].std()
df_degree_2013['stad_degree'] = (df_degree_2013['degree_centrality'] - df_degree_2013['degree_centrality'].mean())/df_degree_2013['degree_centrality'].std()
df_degree_2015['stad_degree'] = (df_degree_2015['degree_centrality'] - df_degree_2015['degree_centrality'].mean())/df_degree_2015['degree_centrality'].std()
df_degree_2018['stad_degree'] = (df_degree_2018['degree_centrality'] - df_degree_2018['degree_centrality'].mean())/df_degree_2018['degree_centrality'].std()

df_degree_2008['year'] = 2009 
df_degree_2011['year'] = 2012
df_degree_2013['year'] = 2014
df_degree_2015['year'] = 2016
df_degree_2018['year'] = 2019

df_eigen_centrality = df_eigen_2008.append([df_eigen_2011, df_eigen_2013, df_eigen_2015, df_eigen_2018])

df_harmnic_centrality = df_harmnic_2008.append([df_harmnic_2011, df_harmnic_2013, df_harmnic_2015, df_harmnic_2018])

df_betweenness_centrality = df_betweenness_2008.append([df_betweenness_2011, df_betweenness_2013, df_betweenness_2015, df_betweenness_2018])

df_degree_centrality = df_degree_2008.append([df_degree_2011, df_degree_2013, df_degree_2015, df_degree_2018])

# Merging data 
ctrlity_frame = [df_eigen_centrality, df_harmnic_centrality, df_betweenness_centrality, df_degree_centrality]
ctrlity_merged = reduce(lambda left,right: pd.merge(left, right, on=['ctry', 'year'],
                                            how='inner'), ctrlity_frame).fillna('0')

ctrlity_merged.to_csv("/content/drive/MyDrive/G11-MEA-Diffusion/dataMEA_Ctrlity/ctrlity_output.csv")

"""### visualization"""

#eigenvector centrality

ee, x = gt.eigenvector(gt_2018_univ)
#x.a /= x.a.max() / 5
#x.a = (x.a + 4.3)**2.8
x.a /= (x.a*10 - 0.7)/0.04 # follow the formula in the book 
gt.graph_draw(gt_2018_univ, vertex_fill_color=x, vcmap=matplotlib.cm.gist_earth, vorder=x) #

gc = gt.GraphView(gt_2018_univ, vfilt=gt.label_largest_component(gt_2018_univ))
c = gt.closeness(gc)
c.a /= c.a / 232
gt.graph_draw(gc, vertex_fill_color=c, vcmap=matplotlib.cm.Oranges, vorder=c)

#betweenness centrality 

bv, be = betweenness(gt_2018_univ)
be.a /= be.a.max() / 5 - 132
graph_draw(gt_2018_univ, pos=None, vertex_fill_color=bv, vcmap=matplotlib.cm.summer)

deg = gt_2018_univ.degree_property_map("total")
gt.graph_draw(gt_2018_univ, vertex_fill_color=deg, vorder=deg)

# https://colab.research.google.com/github/count0/colab-gt/blob/master/colab-gt.ipynb#scrollTo=6km1lWMF2kAm

!apt-get install

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
