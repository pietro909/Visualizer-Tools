'''
	materials.py
	functions used for access and manage materials
'''

import bpy


#rebuild mbe's lists 
def mbeLists() :
	"""
	Collect "material by element" list in the scene
	and return into a set.
	"""	
	mbe_set=set()
	for m in bpy.data.materials :		#for every material
		mbe_set.add(m.mbe)	#append list's name to the set
		
	return mbe_set

#select objects belonging to a list
def selectObjByMbeList(mbe_list) :
	"""
	Select all objects belonging to active mbe list.
	"""	
	mats=bpy.data.materials
	matter=[]
	
	i=0 #counter
	
	for m in mats :
		if m.mbe == mbe_list :
			matter.append(m)
	for obj in bpy.context.scene.objects :
		if obj.type == 'MESH' :
			if obj.active_material in matter :
				obj.select=True
				i+=1
	return i

	
