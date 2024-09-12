import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np
import tkinter as tk
import copy	

max_cluster_value = 500

def cluster_update(cluster, cluster_content, dim):
	k = len(cluster)
	for i in range(k): #по i кластерам
		for q in range(dim): #по q параметрам
			updated_parameter = 0
			for j in range(len(cluster_content[i])): 
				updated_parameter += cluster_content[i][j][q]
			if len(cluster_content[i]) != 0:
				updated_parameter = updated_parameter / len(cluster_content[i])
			cluster[i][q] = updated_parameter
	return cluster


def clusterization(array, k): 
	dim = len(array[0])  

	cluster = [[0 for i in range(dim)] for q in range(k)] 
	cluster_content = [[] for i in range(k)] 

	for i in range(dim):
		for q in range(k):
			cluster[q][i] =np.random.randint(0, max_cluster_value) 

	cluster_content = data_distribution(array, cluster,k,dim)

	privious_cluster = copy.deepcopy(cluster)
	while 1:
		cluster = cluster_update(cluster, cluster_content, dim)
		cluster_content = data_distribution(array, cluster,k, dim)
		if cluster == privious_cluster:
			break
		privious_cluster = copy.deepcopy(cluster)
	draw_dots(cluster,cluster_content)

		
	#visualisation_2d(cluster_content)		

	
def data_distribution(array, cluster,k,dim): 
	n = len(array)
	cluster_content = [[] for i in range(k)]     
    
	for i in range(n):
		min_distance = float('inf')
		situable_cluster = -1
		for j in range(k):
			distance = 0
			for q in range(dim):
				distance += (array[i][q]-cluster[j][q])**2
						
			distance = distance**(1/2)
			if distance < min_distance:
				min_distance = distance
				situable_cluster = j

		cluster_content[situable_cluster].append(array[i])
		
	return cluster_content


#clusterization(array,10)
colors = [
    "#FF0000",  "#00FF00",  "#0000FF", "#FFFF00", "#FFA500", "#800080",  
    "#00FFFF",  "#FF00FF",  "#FF69B4", "#8B4513", "#808080", "#000000", 
    "#777777",  "#000000",  "#FFA500", "#00FF00", "#0000FF", "#FF00FF", 
    "#FFFF00",  "#00FFFF",  "#800080", "#008080", "#808080", "#FF0000"]

def draw_dots(centroids, clusters):
    global canvas
    canvas.delete("all")
    r1 = 3
    r2 = 7
    i = 0
    for cluster in clusters:
        for dot in cluster:
            x, y = dot
            canvas.create_oval(x-r1, y-r1, x+r1, y+r1, fill=colors[i])
        i += 1
        if i == len(colors):
            i = 0

    i = 0
    for dot in centroids:
        x, y = dot
        canvas.create_oval(x-r2, y-r2, x+r2, y+r2, fill="black")
        i += 1
        if i == len(colors):
            i = 0
	
			
prototypes=[]
cluster=[]
T=0
flag=True


def Dist(x1,x2:list[list]):
	distance = ((x1[0]-x2[0])**2) + ((x1[1]-x2[1])**2)				
	distance = distance**(1/2)
	return distance


def find_max_dist(array:list[list],center_cluster)->list[list]:
	max_distance = 0
	for i in range(len(array)):
		distance = Dist(array[i],center_cluster)
		if distance>max_distance:
			max_distance = distance
			new_cluster = array[i]
	print(max_distance)
	return [new_cluster,max_distance]


def clusterization_2(array,k,n,prototypes:list):
	clusters =[[prototypes[i]] for i in range(k)]

	for i in range(n):
		min_distance = float('inf')
		situable_cluster = -1
		for j in range(k):
			dist = Dist(array[i],prototypes[j])
			if dist < min_distance:
				situable_cluster = j
				min_distance=dist
		clusters[situable_cluster].append(array[i])

	return clusters

def new_T(prototypes:list):
	result =0
	k=0
	for i in range(len(prototypes)):
		for j in range(i+1,len(prototypes)):
			result +=Dist(prototypes[i],prototypes[j])
			k+=1
	return result/(2*k)


def maximin(array):
	n = len(array)
	tmp = array[np.random.randint(0,n)]
	global cluster 
	cluster =[[tmp]] 
	global prototypes
	prototypes=[tmp] 
	global T
	global flag
	new = find_max_dist(array,cluster[0][0])
	prototypes.append(new[0])
	T = new[1]/2
	cluster =clusterization_2(array,len(prototypes),n,prototypes)
	draw_dots(prototypes,cluster)
	root.update_idletasks()


def Step(n):
	global prototypes
	global cluster
	global T
	global flag
	if flag:

		new_clusters=[]
		for i in range(len(prototypes)):
			new_clusters.append(find_max_dist(cluster[i],prototypes[i]))

		if len(new_clusters)!=0:
			flag = False
		for i in range(len(new_clusters)):
			if T<new_clusters[i][1]:
				flag=True
				new = new_clusters[i][0]
				prototypes.append(new)	
				break
		cluster = clusterization_2(array,len(prototypes),n,prototypes)		
		draw_dots(prototypes,cluster)
		root.update_idletasks()
		T = new_T(prototypes)
		
	draw_dots(prototypes,cluster)
	root.update_idletasks()	


array = np.random.rand(6000, 2) * 500 

def startK():
	clusterization(array,7)

def start():
	maximin(array)

def Step1():
	btn2.config(state=tk.DISABLED)
	n=len(array)
	Step(n)	
	btn2.config(state=tk.NORMAL)

root = tk.Tk()
root.title("k")
root.geometry("600x600+400+0")
 


canvas = tk.Canvas(root,bg="white", width=500, height=500)
canvas.pack(anchor=tk.CENTER, expand=1)

btn = tk.Button(text='Maximin',command=start)
btn.pack()

btn1 = tk.Button(text='K_means',command=startK)
btn1.pack()

btn2 = tk.Button(text='step',command=Step1)
btn2.pack()
 
root.mainloop()