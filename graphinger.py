#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Title : graphinger
# Author Original : Maximilien Danisch
# Contributor : Viala Axel
# Last edition time : 17-04-2013
#
# Goal : Making a representation of a community
# graph arround a node, please use the Carop algorithm
# develloped by Maximilien before using for good visualisations.
# Usage : graphinger.py "dir(s)" or graphinger.py "file(s)"
#
# Develloped at Lip6 for an internship in Complex Networks team.
# This is a research purpose script use it at your own responsability
#
# With the Maximilien Danisch autorisation for modification,
# relicencing or everything on these script.
#
# Copyright © 2013 Axel Viala <darnuria@lavabit.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.
#

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import codecs
from os import listdir
from os.path import isfile
from sys import exit
from string import split, join

def ploting(data, IDNode, labels, stats,delNode=False):
    filenameResult = "{}.png".format(data)
    new_neighbors = []
    Graph = nx.Graph(nx.read_edgelist(data,
                                      nodetype = int))
    neighbors = Graph.neighbors(IDNode)
    if labels :
        Graph = addLabel(Graph, labels)
    Graph = addData(Graph, neighbors, "color", "green")
    neighborsLen = len(neighbors)
    nodesLen = nx.number_of_nodes(Graph)

    # Still in dev
    # stat(Graph, IDNode, neighbors, neighborsLen, nodesLen)

    if delNode:
        # logging.info("\tDeleting : %d.",IDNode)
        print("\tDeleting : {}.".format(IDNode))
        Graph.remove_node(IDNode)
        Graph = eliminateAloneNode(Graph)
        for node in neighbors:
            if node in Graph.nodes():
                new_neighbors.append(node)
        else:
            new_neighborsLen = len(new_neighbors) # Number of direct nodes after
            neighbors = new_neighbors
        filenameResult = "less_{}_{}".format(IDNode,
                                               filenameResult)# Modify the name.

        # stat(Graph, IDNode, neighbors, neighborsLen, nodesLen)
    # writeGraph(Graph, data, "gml")
    # gml or gexf have some probleme with utf8 encoding.
    # pos = nx.spring_layout(Graph)
    drawing(Graph, nx.spring_layout(Graph),
            IDNode, neighbors, filenameResult)

def stat(Graph, IDNode, neighbors, neighborsLen, nodesLen):
    print("-" * 42)
    print("Statisticals : ")
    rateNeighbors = (float(len(neighbors)) /
                     float(nx.number_of_nodes(Graph))) * 100
    print("\tDirectly connected to {} : {}->{}%.".format(
            IDNode,
            len(neighbors),
            rateNeighbors))
    print("\tNodes : {}, Edges : {}, Neighbors of {} : {}.".format(
            nx.number_of_nodes(Graph),
            nx.number_of_edges(Graph),
            IDNode,
            rateNeighbors)) # Control.
    if len(neighbors) != neighborsLen :
        print("-" * 42)
        print("\tAfter deleting {0} : ".format(IDNode))
        deletedNeighbors = neighborsLen - len(neighbors)
        rateDeleted = float(deletedNeighbors) / float(neighborsLen) * 100
        rateDeletedTotal =  float(deletedNeighbors) / float(nodesLen) * 100
        print("""\t{} Alones nodes deleted
\tRate deletedNeighbors/totalNeighbors : {}%.""".format(deletedNeighbors,
                                                       rateDeleted))
    print("-" * 42)

def drawing(Graph, pos, IDNode, neighbors, filenameResult):
    nx.draw_networkx_nodes(Graph, pos,
                           node_size = 40)
    nx.draw_networkx_nodes(Graph, pos,
                           nodelist = neighbors,
                           node_color = 'g',
                           node_size = 40)
    nx.draw_networkx_edges(Graph,pos,
                           alpha = 0.3)
    # nx.draw_networkx_labels(Graph, pos, labels = dict(
    #        (n[0], n[1]['label']) for n in Graph.nodes(data=True)))
    # Too much information see it with tulip. :/
    plt.axis("off")
    # logging.info("\tFactoring %s.", filenameResult)
    print("\tFactoring {0}.".format(filenameResult))
    # plt.savefig(filenameResult) # Add making dir?
    plt.show()

def eliminateAloneNode(Graph):
    for node in Graph.nodes():
        nodeDegree = nx.degree(Graph, node)
        if nodeDegree == 0:
            Graph.remove_node(node)
    return Graph

def addData(Graph, NodeList ,typeInfo, info):
    for node in NodeList:
        Graph.node[node][typeInfo] = info
    return Graph

def addLabel(Graph, labelList):
    labelFile = open(labelList, 'r')
    labelLines = labelFile.readlines()
    labelFile.close()
    # A little bit greedy.
    # !! FixMe : Using a generator or keyword yield?
    for node in Graph.nodes():
        try:
            label = split(labelLines[node])
            #print("numNode : {0}, label : {1}".format(
            #        label[0], u" ".join(label[1:])))
            # !! FixMe : logging module?
            Graph.node[node]["label"] = u" ".join(label[1:])
        except UnicodeEncodeError, error:
            print("Error Context : {0}".format(label))
            # !! FixMe : using logging module?
            print(error)
    return Graph

# Problems with multiple Encoding in the data file.
# So it's impossible at the moment to export correctly the file.
def writeGraph(Graph, name, filetype):
    if filetype == "gml":
        # logging.info("Write %s.%s", name, filetype)
        print("Write {}.gml".format(name))
        nx.write_gml(Graph, name + ".gml")
    else:
        # logging.info("%s is not a valid filetype, please use gml.", filetype)
        print("{} is not a valid filetype, please use gml.".format(filetype))

HELP = {
    'description': "Visualisation script, with node deletion.",
    'dataset': "File or folder with datafile to processing.",
    'stats': "Feature still in develloppement : Present statisics of the graph",
    'node': "Node where the comunity detection has been launched, "
    "this node will be deleted",
    'labels': "Precise a file with the labels names for each nodes."
    "like ex : 1524522 Potatoe."
    }

def main():
    parser = argparse.ArgumentParser(description=HELP['description'])
    parser.add_argument("dataset",
                    type=str,
                    nargs="+",
                    help=HELP['dataset'],
                     )
    parser.add_argument('-n',"--node",
                        type=int,
                        default=1570174, # Biology in the Dataset.
                        nargs='+',
                        help=HELP['node'])
    parser.add_argument('-s', "--stats",
                    type=bool,
                    dest="stats",
                    help=HELP['stats'],
                     )
    parser.add_argument('-l', "--labels",
                        type=str,
                        dest="labels",
                        help=HELP['labels']
                        )
    args = parser.parse_args()
    print(args.dataset)
    for i, data in enumerate(args.dataset):
        if isfile(data):
            print("Processing {0}.".format(data))
            print("\tPloting without ID : {}.".format(args.node))
            ploting(data, args.node, args.labels,
                    args.stats ,delNode=True)
        else:
            data_files = listdir(data)
            for data_file in data_files:
                if isfile(data_file):
                    print("Processing {}.".format(data_file))
                    print("\tPloting without ID : {}.".format(args.node))
                    ploting(data, args.node, args.labels,
                            args.stats ,delNode=True)
                else:
                    print("\t{} is not a file. Work aborded.".format(data))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    exit(0)
