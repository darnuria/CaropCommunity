#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Title : graphinger
# Author : Maximilien Danisch
# Contributor : Viala Axel
# Last edition time : 27-02-2013
#
# Goal : Making a representation of a graph
# Usage : graphinger.py "dir(s)" or graphinger.py "file(s)"
#
# Develloped at Lip6 for Complex Networks project.
#

import networkx as nx
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile
import sys
from string import split, join
import codecs

def ploting(data, IDNode, delNode = False):
    filenameResult = "{0}.png".format(data) # Name of the picture.
    new_neighbors = []
    Graph = nx.Graph(nx.read_edgelist(data,
                                      nodetype = int))
    neighbors = Graph.neighbors(IDNode)
    Graph = addLabel(Graph, "IDname.txt")
    Graph = addData(Graph, neighbors, "color", "green")
    neighborsLen = len(neighbors)
    nodesLen = nx.number_of_nodes(Graph)

    stat(Graph, IDNode, neighbors, neighborsLen, nodesLen)

    if delNode:
        print("\tDeleting : {0}.".format(IDNode))
        Graph.remove_node(IDNode)
        Graph = eliminateAloneNode(Graph) # Optionnal
        for node in neighbors:
            if node in Graph.nodes():
                new_neighbors.append(node)
        else:
            new_neighborsLen = len(new_neighbors) # Number of direct nodes after
            neighbors = new_neighbors
        filenameResult = "less_{0}_{1}".format(IDNode,
                                               filenameResult) # Modify the name.
        stat(Graph, IDNode, neighbors, neighborsLen, nodesLen)
    #writeGraph(Graph, data, "gml") # gml or gexf
    #pos = nx.spring_layout(Graph)
    drawing(Graph, nx.spring_layout(Graph),
            IDNode, neighbors, filenameResult)
# End main

def stat(Graph, IDNode, neighbors, neighborsLen, nodesLen):
    print("-------------------------------------------")
    print("Statisticals : ")
    rateNeighbors = (float(len(neighbors)) /
                     float(nx.number_of_nodes(Graph))) * 100
    print("\tDirectly connected to {0} : {1}->{2}%.".format(
            IDNode,
            len(neighbors),
            rateNeighbors))
    print("\tNodes : {0}, Edges : {1}, Neighbors of {2} : {3}.".format(
            nx.number_of_nodes(Graph),
            nx.number_of_edges(Graph),
            IDNode,
            rateNeighbors)) # Control.
    if len(neighbors) != neighborsLen :
        print("-------------------------------------------")
        print("\tAfter deleting {0} : ".format(IDNode))
        deletedNeighbors = neighborsLen - len(neighbors)
        rateDeleted = float(deletedNeighbors) / float(neighborsLen) * 100
        rateDeletedTotal =  float(deletedNeighbors) / float(nodesLen) * 100
        print("""\t{0} Alones nodes deleted
\tRate deletedNeighbors/totalNeighbors : {1}%.""".format(deletedNeighbors,
                                                       rateDeleted))
    print("-------------------------------------------")
# End stat

def drawing(Graph, pos, IDNode, neighbors, filenameResult):
    nx.draw_networkx_nodes(Graph, pos,
                           node_size = 40)
    nx.draw_networkx_nodes(Graph, pos,
                           nodelist = neighbors,
                           node_color = 'g',
                           node_size = 40)
    nx.draw_networkx_edges(Graph,pos,
                           alpha = 0.3)
    #nx.draw_networkx_labels(Graph, pos, labels = dict(
    #        (n[0], n[1]['label']) for n in Graph.nodes(data=True)))
    # Too much information see it in tulip :/
    plt.axis("off")
    print("\tFactoring {0}.".format(filenameResult))
    #plt.savefig(filenameResult) # Add making dir?
    plt.show() #Slow a little the trip.
# End drawing

def eliminateAloneNode(Graph):
    for node in Graph.nodes():
        nodeDegree = nx.degree(Graph, node)
        if nodeDegree == 0:
            Graph.remove_node(node)
    return Graph
# End eliminate

def addData(Graph, NodeList ,typeInfo, info):
    for node in NodeList:
        Graph.node[node][typeInfo] = info
    return Graph
# end addData

def addLabel(Graph, labelList):
    labelFile = codecs.open(labelList, "r", "utf-8")
    #labelFile = open(labelList, 'r')
    labelLines = labelFile.readlines()
    #print(labelLines)
    labelFile.close()
    for node in Graph.nodes():
        try:
            label = split(labelLines[node])
            #print("numNode : {0}, label : {1}".format(
            #        label[0], u" ".join(label[1:])))
            Graph.node[node]["label"] = u" ".join(label[1:])
            # !Multiple encoding in the file...!
            # print(node, unicode(Graph.node[node]["label"]))
            #print("")
        except UnicodeEncodeError, error:
            print("Error Context : {0}".format(label)) #Debuging line
            print(error)
    return Graph
# end addLabel
# DELET

def writeGraph(Graph, name, filetype):
    if filetype == "gml":
        print("Write {0}.gml".format(name))
        nx.write_gml(Graph, name+".gml")
    # elif filetype == "gexf": # Bug actualy with python2...
    #    print("Write {0}.gexf".format(name))
    #   nx.write_gexf(Graph, name+".gexf", prettyprint = True)
    else:
        print("{0} is not a valid filetype, please use gml.".format(filetype))
# end writeGraph

def main(args):
    print('Go Go Algo Go!!')
    label = 1570174
    for i,arg in enumerate(args):
        if isfile(arg):
            print("Processing {0}.".format(arg))
            #ploting(arg, label) # arg is a file.
            print("\tPloting without ID : {0}.".format(label))
            ploting(arg, label, True) # arg is a file
        else:
            files = listdir(arg)
            for data in files:
                if isfile(data):
                    print("Processing {0}.".format(data))
                    #ploting(data, label)
                    print("\tPloting without ID : {0}.".format(label))
                    ploting(data, label, True)
                else:
                    print("\t{0} is not a file. Work aborded.".format(data))
    else :
        print("Work is done.")
# End main

if __name__ == "__main__":
    try:
        main(sys.argv[1:]) # Slicing in order to eliminate argv[0].
    except KeyboardInterrupt:
        sys.exit(0)
    print("Done")
# EOF
