import sys
import os

from collections import defaultdict
import numpy as np

class DataCenter(object):
	"""docstring for DataCenter"""
	def __init__(self, config):
		super(DataCenter, self).__init__()
		self.config = config
		
	def load_dataSet(self, dataSet='cora'):
		if dataSet == 'cora':
			cora_content_file = self.config['file_path.cora_content']
			cora_cite_file = self.config['file_path.cora_cite']

			feat_data = []
			labels = [] # label sequence of node
			node_map = {} # map node to Node_ID
			label_map = {} # map label to Label_ID
			with open(cora_content_file) as fp:
				for i, line in enumerate(fp):

					info = line.strip().split()
					feat_data.append([float(x) for x in info[1:-1]])
					node_map[info[0]] = i
					if not info[-1] in label_map:
						label_map[info[-1]] = len(label_map)
					labels.append(label_map[info[-1]])

			feat_data = np.asarray(feat_data)
			labels = np.asarray(labels, dtype=np.int64)
			print(feat_data)
			print(labels)
			adj_lists = defaultdict(set)



			with open(cora_cite_file) as fp:
				for i, line in enumerate(fp):
					info = line.strip().split()
					assert len(info) == 2
					paper1 = node_map[info[0]]
					paper2 = node_map[info[1]]
					adj_lists[paper1].add(paper2)
					adj_lists[paper2].add(paper1)
				print(adj_lists)

			assert len(feat_data) == len(labels) == len(adj_lists)
			test_indexs, val_indexs, train_indexs = self._split_data(feat_data.shape[0])
			setattr(self, dataSet+'_test', test_indexs)
			setattr(self, dataSet+'_val', val_indexs)
			setattr(self, dataSet+'_train', train_indexs)

			setattr(self, dataSet+'_feats', feat_data)
			setattr(self, dataSet+'_labels', labels)
			setattr(self, dataSet+'_adj_lists', adj_lists)


		elif dataSet == 'UPFD':
			data = np.load("./data/new_spacy_feature.npz")
			data1 = data['data']
			data3 = np.load("./data/node_graph_id.npy")
			data4 = np.load("./data/graph_labels.npy")
			label = dict()
			for i in range(314):
#				print(i)
				label[i] = data4[i]
			labels = []
			for i in data3:
#				print(i)
				labels.append(label[i])
			labels = np.asarray(labels)
			feat_data = []
			for i in range(41054):
				m = []
				for j in range(300):
					m.append(data1[i*300+j])
				feat_data.append(m)
			feat_data = np.asarray(feat_data)
			print(feat_data)


			adj_lists = defaultdict(set)
			UPFD_content_file = self.config['file_path.UPFD_node']
			with open(UPFD_content_file) as fp:
				for i, line in enumerate(fp):
					line = line.replace(',', '')
					info = line.strip().split()
					assert len(info) == 2
					paper1 = int(info[0])
					paper2 = int(info[1])
					adj_lists[paper1].add(paper2)
					adj_lists[paper2].add(paper1)
			print(len(feat_data))
			print(len(labels))
			print(len(adj_lists))
			assert len(feat_data) == len(labels) == len(adj_lists)
			test_indexs, val_indexs, train_indexs = self._split_data(feat_data.shape[0])
			setattr(self, dataSet + '_test', test_indexs)
			setattr(self, dataSet + '_val', val_indexs)
			setattr(self, dataSet + '_train', train_indexs)
			setattr(self, dataSet + '_feats', feat_data)
			setattr(self, dataSet + '_labels', labels)
			setattr(self, dataSet + '_adj_lists', adj_lists)

	def _split_data(self, num_nodes, test_split = 3, val_split = 6):
		rand_indices = np.random.permutation(num_nodes)

		test_size = num_nodes // test_split
		val_size = num_nodes // val_split
		train_size = num_nodes - (test_size + val_size)

		test_indexs = rand_indices[:test_size]
		val_indexs = rand_indices[test_size:(test_size+val_size)]
		train_indexs = rand_indices[(test_size+val_size):]
		
		return test_indexs, val_indexs, train_indexs


