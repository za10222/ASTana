#!usr/bin/python
import filecmp
from ast_Construct import Node,ast_construct
from main2 import getlable1,my_dist1,visittree1
from read_file import parse_file
import os
import ast
import zss
import operator as op

def Filecmp(n1,n2):
    isbool=True
    f1=open(n1)
    f2=open(n2)
    for line1 in f1:
        line2=f2.readline()
        if (line1!=line2):
            isbool=False
            break
    return  isbool

def compare(dir1,dir2):
    fd=open("result1.txt",'a')
    fd.write("compare:"+dir1+" and "+ dir2+'\n')
    #print("compare:"+dir1+" and "+ dir2+'\n')
    t = 0
    result1=0
    result2=0
    nodeNumSum=0
    nodedistSum=0
    editSum=0
    nodenum=[]#文件节点深度
    fsml=[]#文件相似度
    fweight=[]
    nodedist=[]
    for i in range(100):
        nodenum.append(0)
        fsml.append(0)
        fweight.append(0)
        nodedist.append(0)

    root = "D:\\Desktop\\SAT\\"+dir2+"\\sanic\\"
    for rt, dirs, files in os.walk(root):
        for f in files:
            fname = os.path.splitext(f)
            if (op.eq(fname[1], ".py")) == True:
                f1 = os.path.join(rt, f)
                f2 = f1.replace(dir2, dir1)
                astbody = parse_file(f1)
                nroot = Node("root", "root")
                if os.path.exists(f2) == False:
                    t=t+1
                    ast_construct(astbody, nroot)
                    nodenum[t] =visittree1(nroot)
                    nodeNumSum=nodeNumSum+nodenum[t]
                    fsml[t]=0
                    nodedist[t] = nodenum[t]
    print(t)

    root= "D:\\Desktop\\SAT\\"+dir1+"\\sanic\\"
    for rt, dirs, files in os.walk(root):
        for f in files:
            fname = os.path.splitext(f)
            if (op.eq(fname[1], ".py")) == True:
                t=t+1
                print(t)
                f1 = os.path.join(rt, f)
                f2 = f1.replace(dir1, dir2)
                astbody = parse_file(f1)
                if os.path.exists(f2)== True:
                    nroot = Node("root", "root")
                    ast_construct(astbody, nroot)
                    v1 = visittree1(nroot)
                    if filecmp.cmp(f1,f2):
                        nodenum[t] =v1
                        fsml[t]=1
                        nodedist[t] = 0
                        nodeNumSum = nodeNumSum + nodenum[t]
                    else:
                        astbody2 = parse_file(f2)
                        nroot2=Node("root","root")
                        ast_construct(astbody2, nroot2)
                        dist = zss.simple_distance(
                        nroot, nroot2, Node.getchild, getlable1,my_dist1)
                        v2= visittree1(nroot2)
                        if  v1>v2:
                            treenode = v1
                        else:
                            treenode = v2
                        nodenum[t]=treenode
                        nodeNumSum=nodeNumSum+nodenum[t]
                        fsml[t]=1.0 - dist*1.0/treenode
                        nodedist[t] = dist
                else:
                    astbody = parse_file(f1)
                    nroot = Node("root", "root")
                    ast_construct(astbody, nroot)
                    nodenum[t] = visittree1(nroot)
                    nodeNumSum = nodeNumSum + nodenum[t]
                    fsml[t] = 0
                    nodedist[t] = nodenum[t]

    for i in range(1,t+1):
        fweight[i]=nodenum[i]*1.0/nodeNumSum
        result1=result1+fsml[i]
        result2=result2+fweight[i]*fsml[i]
        nodedistSum=nodedist[i]+nodedistSum
        editSum=editSum+nodedist[i]*1.0/nodenum[i]
        #print("file "+ i.__str__()+" : "+"similar:"+fsml[i].__str__()+" nodenum: "+nodenum[i].__str__()+" weight: "+fweight[i].__str__()+'\n')
        fd.write("file "+ i.__str__()+" : "+"similar:"+fsml[i].__str__()+" nodedist: "+nodedist[i].__str__()+" nodenum: "+nodenum[i].__str__()+" weight: "+fweight[i].__str__()+'\n')

    fd.write("this is average result1:\n"+(result1*1.0/t*100).__str__()+"%\n")
    fd.write("this is average result1:\n" + ((1.0-editSum*1.0/t)*100).__str__() + "%\n")
    fd.write("this is weight result1:\n" + (result2 * 1.0* 100).__str__() + "%\n")
    fd.write("this is weight result2:\n" + ((1-nodedistSum*1.0/nodeNumSum)* 100).__str__() + "%\n")
    fd.write('\n')
    fd.close()

    '''
    print("nodeNumSum:"+nodeNumSum.__str__()+'\n')
    print("this is average result:\n"+(result1*1.0/t*100).__str__()+"%\n")
    print("this is weight result:\n" + (result2 * 1.0* 100).__str__()+ "%\n")
    '''
'''
compare("sanic-0.1.2","sanic-0.1.3")
compare("sanic-0.1.3","sanic-0.1.4")
compare("sanic-0.1.4","sanic-0.1.5")
compare("sanic-0.1.5","sanic-0.1.6")
compare("sanic-0.1.6","sanic-0.1.7")
compare("sanic-0.1.7","sanic-0.1.8")
compare("sanic-0.1.8","sanic-0.1.9")
compare("sanic-0.1.9","sanic-0.2.0")
compare("sanic-0.2.0","sanic-0.3.0")
compare("sanic-0.3.0","sanic-0.3.1")
compare("sanic-0.3.1","sanic-0.4.0")
compare("sanic-0.4.0","sanic-0.4.1")
compare("sanic-0.4.1","sanic-0.5.0")
compare("sanic-0.5.0","sanic-0.5.1")
compare("sanic-0.5.1","sanic-0.5.2")
compare("sanic-0.5.3","sanic-0.5.4")
compare("sanic-0.5.4","sanic-0.6.0")
compare("sanic-0.6.0","sanic-0.7.0")
compare("sanic-0.7.0","sanic-0.8.0")
compare("sanic-0.8.0","sanic-0.8.1")
compare("sanic-0.8.1","sanic-0.8.2")
compare("sanic-0.8.2","sanic-0.8.3")
'''
compare("sanic-c1","sanic-c2")
compare("sanic-c2","sanic-c3")
compare("sanic-c3","sanic-c4")
compare("sanic-c4","sanic-c5")
compare("sanic-c5","sanic-c6")
compare("sanic-c6","sanic-c7")
compare("sanic-c7","sanic-c8")
compare("sanic-c8","sanic-c9")
compare("sanic-c9","sanic-c10")
compare("sanic-c10","sanic-c11")
compare("sanic-c11","sanic-c12")
compare("sanic-c12","sanic-c13")
compare("sanic-c13","sanic-c14")
compare("sanic-c14","sanic-c15")
compare("sanic-c15","sanic-c16")
compare("sanic-c16","sanic-c17")
compare("sanic-c17","sanic-c18")
compare("sanic-c18","sanic-c19")
compare("sanic-c19","sanic-c20")

