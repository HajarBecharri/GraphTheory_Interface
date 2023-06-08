import tkinter as tk
from tkinter import *
from collections import namedtuple
from pyvis.network import Network
from IPython.core.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt

Graph=namedtuple("Graph",["nodes","edges","is_directed"])

class inteface:
    
    def __init__(self,master) :
        master.title("TheoryGraphInterface")
        master.geometry("{}x{}+{}+{}".format(400,500,0,0))
        master.config(bg='black')
        master.resizable(height=False,width=False)
        self.main_frame=Frame(bg='#fff')
        self.main_frame.pack(side=TOP)
        self.main_frame.pack_propagate(False)
        self.main_frame.config(width=400,height=500)
        self.entre=StringVar()
        self.home_frame=Frame(self.main_frame,bg='#fff')
        self.home_frame.pack(side=TOP)
        self.home_frame.pack_propagate(False)
        self.home_frame.config(width=400,height=500)
        self.entre=StringVar()
        self.nodes=[]
        self.myliste_adj={}
        self.myedges=[]
        self.dirradio=IntVar()
        self.pondradio=IntVar()
        self.E=0
        self.poids=[]
        self.primMatrix=[]
        self.k=0
        
        
        Label(self.home_frame,height=2,text="le nombre du sommets:",fg='black',bg='#fff').place(x=8,y=15)
        Entry(self.home_frame,width=8,bg='#fff',font=('Arial Bold',28),textvariable=self.entre).place(x=180,y=15)
        rd1=Radiobutton(self.home_frame,text="directed",bg="white",variable=self.dirradio, value=1)
        rd1.place(x=5,y=70)
        rd2=Radiobutton(self.home_frame,text="Notdirected",bg="white",variable=self.dirradio,value=0)
        rd2.place(x=85,y=70)
        rp1=Radiobutton(self.home_frame,text="pondered" ,bg="white",variable=self.pondradio, value=1)
        rp1.place(x=165,y=70)
        rp2=Radiobutton(self.home_frame,text="notpondered",bg="white",variable=self.pondradio,value=0)
        rp2.place(x=255,y=70)
        Button(self.home_frame,width=5,height=1,text='entrer',relief='flat',bg='red',command=lambda:self.matrix()).place(x=300,y=100)

# la page du remplissage de la matrice
    def matrix(self):
      
      self.isdirected=self.dirradio.get()
      self.ispondered=self.pondradio.get()
      
      Label(self.home_frame,height=1,text="Veillez remplir la matrice :",fg='#eee',bg='black').place(x=60,y=120)
      self.sommet=int(self.entre.get())
      self.m=StringVar()
      self.m=[[0 for i in range(self.sommet)]for i in range(self.sommet)]
      self.matrix=[]
      self.G=Graph(self.nodes,self.myedges,self.isdirected)
      for i in range(self.sommet):
          row=[]
          for j in range(self.sommet):
            if(i==0):
             e=tk.Entry(self.home_frame,width=2,bg='#71BDFF',font=('Arial Bold',28))
             e.place(x=60*(j+1),y=160) 
             row.append(e)
            else:
             e=tk.Entry(self.home_frame,width=2,bg='#71BDFF',font=('Arial Bold',28))
             e.place(x=60*(j+1),y=160+(80*(i)))
             row.append(e)
          self.matrix.append(row)
          if(i==self.sommet-1):
             Button(self.home_frame,width=5,height=1,text='submit',relief='flat',bg='red',command=lambda:self.testpondr()).place(x=90,y=230+(80*(i)))
        
      
      
    def getnumArc(self) :
      if(self.isdirected):
        return len(self.myedges)
      else:
        return len(self.myedgesndir)
      
# la page des deux choix   
 
    def choice(self):
     
      
      self.i=0
      if(self.ispondered):
        self.poids=[0 for j in range(self.E)]
        for i in range(self.E):
         self.poids[i]=self.enterPoids[i].get()
        print(self.poids)
        self.i=0
        if(not self.isdirected):
         for edge in self.ponedges:
           edge.append(int(self.poids[self.i]))
           self.i=self.i+1
        print(self.myedgesndir)
        
        self.getDicPond()
        print(self.dicpond)
      
      self.delete_pages()
      choice_frame=Frame(self.main_frame,bg='black')
      choice_frame.pack(side=TOP)
      choice_frame.pack_propagate(False)
      choice_frame.config(width=400,height=500)
      Button(choice_frame,width=20,height=3,text="Afficher Graph",fg='#71BDFF',bg='#fff',command=lambda:self.getGraph()).place(x=40,y=200)
      Button(choice_frame,width=20,height=3,text="Les Algorithms",fg='#71BDFF',bg='#fff',command=lambda:self.algo()).place(x=200,y=200)  







    
  # la page speciale pour choix pondere
    
    def testpondr(self)  :
      
      self.ponedges=[]
      for i in range(self.sommet):
         for j in range(self.sommet):
            self.m[i][j]=self.matrix[i][j].get()
      print(self.m)
      self.node()
      self.edges(self.m)
      for i in self.myedgesndir:
          self.ponedges.append(i)
      print("edggesndir,edgesdir")
      print(self.myedgesndir)
      print(self.myedges)
      self.list_adja(self.nodes,self.myedges)
      print("liste_adj")
      print(self.myliste_adj)
    

      self.E=self.getnumArc()
      self.delete_pages()
      if(self.ispondered) :
        self.enterPoids=[]
        poids_frame=Frame(self.main_frame,bg='black')
        poids_frame.pack(side=TOP)
        poids_frame.pack_propagate(False)
        poids_frame.config(width=400,height=500)
        Label(poids_frame,text="Veuillez entrer les poids :",bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=10,y=10)
        if(self.isdirected):
          self.i=1
          for edge in self.myedges:
             Label(poids_frame,text=edge,bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=10,y=60*(self.i))
             e=tk.Entry(poids_frame,width=2,bg='#71BDFF',font=('Arial Bold',15))
             e.place(x=100,y=60*(self.i)) 
             self.enterPoids.append(e)
             self.i=self.i+1

             if(self.i==self.E):
              Button(poids_frame,width=5,height=1,text='submit',relief='flat',bg='red',command=lambda:self.choice()).place(x=90,y=(90*(self.i))) 
          
        else:
          self.i=1
          for edge in self.myedgesndir:
             Label(poids_frame,text=edge,bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=10,y=60*(self.i))
             e=tk.Entry(poids_frame,width=2,bg='#71BDFF',font=('Arial Bold',15))
             e.place(x=100,y=60*(self.i)) 
             self.enterPoids.append(e)
             self.i=self.i+1

             if(self.i==self.E):
              Button(poids_frame,width=5,height=1,text='submit',relief='flat',bg='red',command=lambda:self.choice()).place(x=90,y=(90*(self.i)))    
             
      else:
        self.choice()       

    def delete_pages(self):
      for frame in self.main_frame.winfo_children():
        frame.destroy()  

# le choix de get Graph

    def getGraph(self):
     if(self.isdirected):
       self.i=0
       g = nx.DiGraph()
       g.add_edges_from(self.myedges)
       if(self.ispondered):
        for e in g.edges:
         g[e[0]][e[1]]['weight'] = self.poids[self.i]  
         self.i=self.i+1
        plt.figure()    
        pos = nx.spring_layout(g)
        weight_labels = nx.get_edge_attributes(g,'weight')
        nx.draw(g,pos,font_color = 'white', node_shape = 's', with_labels = True,)
        nx.draw_networkx_edge_labels(g,pos,edge_labels=weight_labels)
       else:
         nx.draw(g,font_color = 'white', node_shape = 's', with_labels = True,)
         
    
     else:
       self.i=0
       g = nx.Graph()
       g.add_edges_from(self.myedges)
       if(self.ispondered):
        for e in g.edges:
         g[e[0]][e[1]]['weight'] = self.poids[self.i]  
         self.i=self.i+1
     
        plt.figure()    
        pos = nx.spring_layout(g)
        weight_labels = nx.get_edge_attributes(g,'weight')
        nx.draw(g,pos,font_color = 'white', node_shape = 's', with_labels = True,)
        nx.draw_networkx_edge_labels(g,pos,edge_labels=weight_labels) 
       else:
         nx.draw(g,font_color = 'white', node_shape = 's', with_labels = True,)
     
     plt.savefig("Graph.png")


  # la page des algorithms

    def algo(self):
       self.d=[]
       self.s=[]
       self.a=[]
       self.delete_pages()
       algorithm_frame=Frame(self.main_frame,bg='black')
       algorithm_frame.pack(side=TOP)
       algorithm_frame.pack_propagate(False)
       algorithm_frame.config(width=400,height=500)
       Label(algorithm_frame,text="Paccourrir le Graph : départ-> ",bg="black",fg="white",font=('Arial Bold',15)).place(x=10,y=10)
       depart=Entry(algorithm_frame,width=2,bg='#71BDFF',font=('Arial Bold',15))
       depart.place(x=300,y=10)
       self.d.append(depart)
       Button(algorithm_frame,text="DFS",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.DFSS(self.myliste_adj)).place(x=10,y=50)
       Button(algorithm_frame,text="BFS",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.BFS(self.myliste_adj)).place(x=100,y=50)
       Button(algorithm_frame,text="WARSHALL",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.Warshall(self.myliste_adj)).place(x=190,y=50)
       if(self.ispondered):
        if(self.isdirected):
         Label(algorithm_frame,text="shortestPath :",bg="black",fg="white",font=('Arial Bold',15)).place(x=10,y=100)
         Button(algorithm_frame,text="DJKSTRA",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.Djkstra()).place(x=10,y=140)
         Button(algorithm_frame,text="BellmanFord",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.BellmanFord()).place(x=100,y=140)
         Label(algorithm_frame,text="Max Flot : Source|Arrive",bg="black",fg="white",font=('Arial Bold',15)).place(x=10,y=180)
         source=Entry(algorithm_frame,width=2,bg='#71BDFF',font=('Arial Bold',15))
         source.place(x=300,y=180)
         self.s.append(source)
         arrivee=Entry(algorithm_frame,width=2,bg='#71BDFF',font=('Arial Bold',15))
         arrivee.place(x=350,y=180)
         self.a.append(arrivee)
         Button(algorithm_frame,text="Ford Fulkerson",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.ford_fulkerson(self.matricePond,int(self.s[0].get()),int(self.a[0].get()))).place(x=10,y=220)
        else:
         Label(algorithm_frame,text="ACM :",bg="black",fg="white",font=('Arial Bold',15)).place(x=10,y=190)
         Button(algorithm_frame,text="Krustal",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.Krustal()).place(x=10,y=230)
         Button(algorithm_frame,text="Prim",width=10,height=1,fg='#71BDFF',bg='#fff',command=lambda:self.Prim()).place(x=100,y=230)
       

# Array of graph nodes

    def node(self):
     for i in range(self.sommet):
      self.nodes.append(i)

# array of graph edges

    def edges(self,matrix):
     for i in range(self.sommet):
      for j in range(self.sommet):
        
        if(int(matrix[i][j])==1):
         self.myedges.append([i,j])
     
     self.myedgesndir=[]
     for i in range(self.sommet):
      for j in range(self.sommet):
        
        if(int(matrix[i][j])==1 and [j,i] not in self.myedgesndir):
         self.myedgesndir.append([i,j])   

# creation de la liste d adjacente     
    def list_adja(self,nodes,edges):
 
     for node in nodes:
      self.myliste_adj[node]=[]
    
     for edge in edges:
       self.myliste_adj[edge[0]].append(edge[1])

# recuperation du dictionnaire pondere et matrice ponderee
    def getDicPond(self):
        
    
        self.dicpond={}
        self.matricePond=[[0 for i in range(self.sommet)]for i in range(self.sommet)]
        i=0
        if(self.isdirected):
         for edge in self.myedges:
          self.dicpond[tuple(edge)]=self.poids[i]
          i+=1
          self.k=0
        else:
           
           for i in range(self.sommet):
             for j in range(self.sommet):
              
              if(j in self.myliste_adj[i]):
               if((i,j) not in self.dicpond ):

                self.dicpond[(i,j)]=self.poids[self.k]
                self.dicpond[(j,i)]=self.poids[self.k]
                self.k+=1
                
        for i in range(self.sommet):
             for j in range(self.sommet):
               for key,value in self.dicpond.items():
                 if(key==(i,j)):
                   self.matricePond[i][j]=int(value)
                   

        print(self.dicpond)
        print(self.matricePond)



        
        
#DFS Algorithm

    def DFSS(self,graph):
      
      self.DfsVisited=[]
      node=int(self.d[0].get())
      self.DFS(self.DfsVisited,graph,node)
      
      self.delete_pages()
      Bellman_frame=Frame(self.main_frame,bg='black')
      Bellman_frame.pack(side=TOP)
      Bellman_frame.pack_propagate(False)
      Bellman_frame.config(width=400,height=500)
      
      for i in range(len(self.DfsVisited)):
       Label(Bellman_frame,text=str(self.DfsVisited[i])+"-->",bg="white",fg="#71BDFF",font=('Arial Bold',20)).place(x=20+(i*30),y=20)
      Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)
    def DFS(self,visited,graph,node):
      if node not in visited:
       visited.append(node)
       print(node,end="->")

       for neibour in graph[node]:
        self.DFS(visited,graph,int(neibour))
      



#BFS Algorithm

    def BFS(self,graph):
      node=int(self.d[0].get())
      
      self.BfsVisited=[]
      queue=[]
      self.BfsVisited.append(node)
      queue.append(node)

      while queue:
        m=queue.pop(0)
        print(m,end="->")

        for neibour in graph[m]:
            if neibour not in self.BfsVisited:
                self.BfsVisited.append(neibour)
     
                queue.append(neibour)
      print(self.BfsVisited)  

      self.delete_pages()
      Bellman_frame=Frame(self.main_frame,bg='black')
      Bellman_frame.pack(side=TOP)
      Bellman_frame.pack_propagate(False)
      Bellman_frame.config(width=400,height=500)
      for i in range(len(self.BfsVisited)):
       Label(Bellman_frame,text=str(self.BfsVisited[i])+"-->",bg="white",fg="#71BDFF",font=('Arial Bold',20)).place(x=20+(i*30),y=20)

      Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)


#warshall Algorithm

    def Warshall(self,graph):
      self.Warshall_edg=[]
      self.Warshall_dic=graph
      self.connexe=True
      for sommet in self.Warshall_dic:
        for key,values in self.Warshall_dic.items():
          if(not key==sommet):
            for value in values:
              if value==sommet:
                for sort in self.Warshall_dic[sommet]:
                  if(not sort==sommet):
                    if sort not in self.Warshall_dic[key]:
                     self.Warshall_dic[key].append(sort)
      for v in self.nodes: 
        for i in self.nodes:
          if(i not in self.Warshall_dic[v]):
            self.connexe=False
      for v,values in self.Warshall_dic.items():
        for value in values:
          if (v,value) not in self.Warshall_edg:
            self.Warshall_edg.append((v,value))
      g = nx.DiGraph()
      g.add_edges_from(self.Warshall_edg)
      nx.draw(g,font_color = 'white', node_shape = 's', with_labels = True,)
      plt.savefig("warshall.png")
      self.delete_pages()
      Bellman_frame=Frame(self.main_frame,bg='black')
      Bellman_frame.pack(side=TOP)
      Bellman_frame.pack_propagate(False)
      Bellman_frame.config(width=400,height=500)
      if(self.connexe):
       Label(Bellman_frame,text='le graph transitive est complet alors le graph donné est connexe',bg="black",fg="#71BDFF",font=('Arial Bold',8)).place(x=20,y=20)
      else:
       Label(Bellman_frame,text='le graph transitive est non complet alors le graph donné est non connexe',bg="black",fg="#71BDFF",font=('Arial Bold',8)).place(x=20,y=20)

      Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)



# Krustal Algorithm 

    def Krustal(self):
      self.krustal_node=[]
      self.krustal_edges=[]
      print(self.myedgesndir)
      ordered_edges= sorted(self.myedgesndir, key=lambda item: item[2])
      print(ordered_edges)
      for edge in ordered_edges:
       if edge[0] not in self.krustal_node:
         if edge[1] not in self.krustal_node:
          self.krustal_edges.append(edge)
          self.krustal_node.append(edge[0])
          self.krustal_node.append(edge[1])
       else:
        if edge[1] not in self.krustal_node:
          self.krustal_edges.append(edge)
          self.krustal_node.append(edge[1])
      g = nx.Graph()
      g.add_weighted_edges_from(self.krustal_edges)
      plt.figure()    
      pos = nx.spring_layout(g)
      weight_labels = nx.get_edge_attributes(g,'weight')
      print(weight_labels)
      nx.draw(g,pos,font_color = 'white', node_shape = 's', with_labels = True,)
      nx.draw_networkx_edge_labels(g,pos,edge_labels=weight_labels) 
      plt.savefig("krustal.png")



# Prim Algorithm

    def Prim(self) :
      visited=[]
      visited = [0 for i in range(self.sommet)] 
      edgeNum=0
      visited[0]=True
      while edgeNum<self.sommet-1:
        min=float('inf')
        for i in range(self.sommet):
          if (visited[i]):
            for j in range(self.sommet):
              if(not visited[j] and self.m[i][j]):
                if( min > float(self.dicpond[(i,j)])):
                 min=float(self.dicpond[(i,j)])
                 s=i
                 d=j
        self.primMatrix.append((s,d,int(self.dicpond[(s,d)])))
        visited[d]=True
        edgeNum+=1
      print(self.primMatrix)
      g = nx.Graph()
      g.add_weighted_edges_from(self.primMatrix)
      plt.figure()    
      pos = nx.spring_layout(g)
      weight_labels = nx.get_edge_attributes(g,'weight')
      print(weight_labels)
      nx.draw(g,pos,font_color = 'white', node_shape = 's', with_labels = True,)
      nx.draw_networkx_edge_labels(g,pos,edge_labels=weight_labels) 
      plt.savefig("Prim.png")



#Djkstra Algorithm

    def Djkstra(self):
      self.path_lenth={v:float('inf') for v in self.nodes}
      self.path_lenth[0]=0
      self.path_source={v:'N' for v in self.nodes}
      self.path_source[0]='-'
      self.adjacent_pond={v:{} for v in self.nodes}
      for (u,v),k in self.dicpond.items():
        self.adjacent_pond[u][v]=k
        if(not self.isdirected):
          self.adjacent_pond[v][u]=k
      self.temporary_nodes=[v for v in self.nodes]
      while(len(self.temporary_nodes)>0):
        upper_bounds={v:self.path_lenth[v] for v in self.temporary_nodes}
        u=min(upper_bounds,key=upper_bounds.get)
        self.temporary_nodes.remove(u)

        for v,k in self.adjacent_pond[u].items():
          if(self.path_lenth[v]>self.path_lenth[u]+int(k)):
             self.path_lenth[v]=self.path_lenth[u]+int(k)
             self.path_source[v]=u
      self.delete_pages()
      Bellman_frame=Frame(self.main_frame,bg='black')
      Bellman_frame.pack(side=TOP)
      Bellman_frame.pack_propagate(False)
      Bellman_frame.config(width=400,height=500)
      Label(Bellman_frame,text='la table de Djkstra:',bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=60,y=20)
      Label(Bellman_frame,text='L',bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=60,y=90)
      Label(Bellman_frame,text='P',bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=60,y=120)
      self.x=90
      for u in range(self.sommet):
         Label(Bellman_frame,text=u,width=2,height=1,bg="white",fg="black",font=('Arial Bold',15)).place(x=self.x,y=60)
         self.x+=30
      self.x=90
      for u,v in self.path_lenth.items():
        Label(Bellman_frame,text=v,width=2,height=1,bg="white",fg="black",font=('Arial Bold',15)).place(x=self.x,y=90)
        self.x+=30
      self.x=90
      for u,v in self.path_source.items():
        Label(Bellman_frame,text=v,bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=self.x,y=120)
        self.x+=30

      Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)
       
#Bellman Ford Algorithm 

    def BellmanFord(self):
      self.path_lenth={v:float('inf') for v in self.nodes}
      self.path_source={v:'N' for v in self.nodes}
      self.path_source[0]='-'
      self.path_lenth[0]=0
      i=0
      for i in range(self.sommet):
        for (u,v),k in self.dicpond.items():
          if(self.path_lenth[v]>self.path_lenth[u]+int(k)):
            self.path_lenth[v]=self.path_lenth[u]+int(k)
            self.path_source[v]=u

      self.nonCircuitFord=True
      for (u,v),k in self.dicpond.items():
          if(self.path_lenth[v]>self.path_lenth[u]+int(k)):
            self.nonCircuitFord=False

      if(self.nonCircuitFord==True):
       
       self.delete_pages()
       Bellman_frame=Frame(self.main_frame,bg='black')
       Bellman_frame.pack(side=TOP)
       Bellman_frame.pack_propagate(False)
       Bellman_frame.config(width=400,height=500)
       Label(Bellman_frame,text='la table de BellmanFord:',bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=60,y=20)
       Label(Bellman_frame,text='L',bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=60,y=90)
       Label(Bellman_frame,text='P',bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=60,y=120)
       self.x=90
       for u in range(self.sommet):
         Label(Bellman_frame,text=u,width=2,height=1,bg="white",fg="black",font=('Arial Bold',15)).place(x=self.x,y=60)
         self.x+=30
       self.x=90
       for u,v in self.path_lenth.items():
        Label(Bellman_frame,text=v,width=2,height=1,bg="white",fg="black",font=('Arial Bold',15)).place(x=self.x,y=90)
        self.x+=30
       self.x=90
       for u,v in self.path_source.items():
        Label(Bellman_frame,text=v,bg="white",width=2,height=1,fg="black",font=('Arial Bold',15)).place(x=self.x,y=120)
        self.x+=30
       
      else:
        print("circuit absorbant")


      Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)


      
      #self.Warshall



# Ford Fulkerson Algorithm

    #part 1
    def searching_algo_BFS(self,graph,s, t, parent):
        row=len(graph)
        visited = [False] * (row)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False
    
    #part 2
    def ford_fulkerson(self,graph, source, sink):
        row=len(graph)
        parent = [-1] * (row)
        max_flow = 0

        while self.searching_algo_BFS(graph,source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow,graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                graph[u][v] -= path_flow
                graph[v][u] += path_flow
                v = parent[v]

        self.delete_pages()
        Bellman_frame=Frame(self.main_frame,bg='black')
        Bellman_frame.pack(side=TOP)
        Bellman_frame.pack_propagate(False)
        Bellman_frame.config(width=400,height=500)
      
        Label(Bellman_frame,text='Le flox maximal est : ' +str(max_flow),bg="black",fg="#71BDFF",font=('Arial Bold',15)).place(x=20,y=20)

        Button(Bellman_frame,text="<--retour",width=10,height=1,fg='green',bg='#fff',command=lambda:self.algo()).place(x=300,y=450)

root=Tk()     
interface=inteface(root)

root.mainloop()
 