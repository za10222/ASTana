#!/usr/bin/python
from read_file import parse_file
import  ast
import operator as op
import zss
from ast_Construct import Node, ast_construct
def visittree(mynode):
    t=1
    for nodes in ast.iter_child_nodes(mynode):
        t=t+visittree(nodes)
    return t

def visittree1(mynode):
    t=1
    for nodes in mynode.children:
        t=t+visittree1(nodes)
    return t
def getlable(myNode):
    t=1
    for field,value in ast.iter_fields(myNode):
        t=field;
    if (t ==1):
          t=myNode.__class__.__name__;
    return t;
def getlable1(myNode):
    return myNode.label+"::"+myNode.value;
def getlist(myNode):
    return list(ast.iter_child_nodes(myNode));

def my_dist(A,B):
    if (op.eq(A,B)):
        return 0
    else:
        return 1

def my_dist1(A, B):
    if(A==""):
        return 1;
    if(B == ""):
        return 1;
    Astr = A.split("::")
    Bstr = B.split("::")
    t = 1;
    if (op.eq(Astr[0],Bstr[0])):
        if(op.eq(Astr[1],Bstr[1])):
            t=0;
        else:
            t=0.7;
    return t;

def print_tree(parent):

    print (parent.label + " " + parent.value)
    if len(parent.children) != 0:
        for child in parent.children:
            print_tree(child)
'''
astbody = parse_file("./main (2).py")
astbody3 = parse_file("./t5.py")
astbody2 = parse_file("./test3.py")
root = Node("root", "root")
ast_construct(astbody, root)
root3 = Node("root", "root")
ast_construct(astbody3, root3)
dist = zss.simple_distance(
    astbody, astbody3, getlist, getlable, my_dist)
print(dist)
print(visittree(astbody))
dist = zss.simple_distance(
    root, root3, Node.getchild, getlable1, my_dist1)
print(dist)
print(visittree1(root))
print(visittree1(root3))
print_tree(root)
'''