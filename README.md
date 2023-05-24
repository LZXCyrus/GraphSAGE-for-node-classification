# A sample of GraphSAGE for node classification
The project contains a sample of node classification task solved by GraphSAGE.

The code is altered based on the previous work of https://github.com/twjiang/graphSAGE-pytorch.

Compared to the previous code, this project adds multiple aggregate functions of Graphsage and a new UPFD dataset for testing.

## Environment

Python==3.8

Pytorch==1.13.1+cu117

## Dataset

If you want to use Cora Dataset, please follow https://github.com/twjiang/graphSAGE-pytorch.

If you want to use UPFD dataset for fake news detection, please dowload the original data and preprocessing by https://github.com/safe-graph/GNN-FakeNews. Then gain the following files:new_spaCy_feature.npz(the feature encoded by spaCy model plus 10 dimensions Profile characteristics), graph_labels.npy (labels for news detection);node_graph_id.npy (showing which news each user node belongs to) , and put them into a folder named data.

experiments.conf is for UPFD dataset.
