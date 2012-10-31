'''
        operators.py
        file with operators definitions, I prefer to keep them here in order to have a cleaner code
        and because it's simpler for me find them
'''

import bpy
import random
import bmesh
from . import materials         #functions for material works

class OBJECT_OT_mbelAssignToSubObj(bpy.types.Operator) :
        """
        Assign random material to linked polygons in current object.
        Materials are choosen from object's material's slots.
        """
        bl_idname = "mbel.assigntosubobj"
        bl_label = "Assign to subobjects"
        
        def execute(self, context) :
                
                mesh = bpy.context.object.data
                obj = bpy.context.active_object
                N=len(bpy.context.active_object.material_slots.items())

                if bpy.context.mode != 'EDIT':            #if not in edit mode
                        curr_mode = obj.mode
                        bpy.ops.object.mode_set(mode='EDIT')

                #bmesh    
                bm = bmesh.from_edit_mesh(mesh)

                #array of faces index
                total_faces = [f.index for f in bm.faces]
                i = 0
                
                #while counter < of face's array's length
                while (i < len(total_faces)) :
                        #take next face
                        bm.faces[total_faces[i]].select_set(1)
                        bpy.ops.mesh.select_linked()            #select linked
                        material_index = random.randint(0,N-1)  #mat ID
                        #for faces in bmesh
                        for face in bm.faces:
                                if face.select :                    #if selected
                                        face.material_index=material_index  #assign ID
                                        total_faces.remove(face.index)      #remove face's index
                                                                                                                #from array    
                        bpy.ops.mesh.select_all(action='TOGGLE')    #deselect all     
                        i += 1  #counter ++

                bpy.ops.object.mode_set(mode=curr_mode)          
                self.report({'INFO'}, str(N)+" materials assigned to "+str(len(total_faces))+" polygons")

                return{'FINISHED'}

class OBJECT_OT_mbelFillSlot(bpy.types.Operator):
        """
        Fill material's slots of current active object with
        current list's material
        """
        bl_idname = "mbel.fillslot"
        bl_label = "Fill material slots with current list's material"
        
        def execute(self, context):
                
                #checking wether active object is a mesh
                if bpy.context.active_object.type != 'MESH' :
                        self.report({'ERROR'}, "Works with MESH only")
                        return{'CANCELLED'}
                
                mats = bpy.data.materials
                
                obj = bpy.context.active_object
                i = 0
                for mat in mats :
                        if mat.mbe == context.scene.mbe_current_list :
                                bpy.ops.object.material_slot_add()
                                obj.material_slots[i].material = mat
                                i+=1
                
                return{'FINISHED'}

class OBJECT_OT_mbelAssignPolys(bpy.types.Operator):
        """
        Assign random material to single polygons in current object.
        Materials are choosen from object's material's slots.
        """
        bl_idname = "mbel.assignpolys"
        bl_label = "Assign random material ID to polygons"
        
        def execute(self, context):

                #checking wether active object is a mesh
                if bpy.context.active_object.type != 'MESH' :
                        self.report({'ERROR'}, "Works with MESH only")
                        return{'CANCELLED'}

                mesh = context.active_object.data
                N = len(context.active_object.material_slots)
                
                for p in mesh.polygons :
                        p.material_index=random.randint(0,N)
                
                self.report({'INFO'}, str(N)+" materials assigned to "+str(p.index)+" polygons")
                
                return{'FINISHED'}           

class OBJECT_OT_viztoolChooseMenu(bpy.types.Operator) :
        """
        Handler for menu selection
        """
        bl_idname = "viztool.choosemenu"
        bl_label = "On list selection"
        
        name = bpy.props.StringProperty() # defining the property
        
        def execute(self, context) :
                bpy.context.scene.mbe_current_list = self.name
                return{'FINISHED'}


class OBJECT_OT_mbelSelMatted(bpy.types.Operator):
        """
        Select objects belonging to current material's list
        """
        bl_idname = "mbel.selmatted"
        bl_label = "Select objects with the same MBE list"
        
        def execute(self, context):
                selected = materials.selectObjByMbeList( context.scene.mbe_current_list )
                return{'FINISHED'}

class OBJECT_OT_mbelAssignMat(bpy.types.Operator):
        """
        Assign random material to every objects in selection.
        Materials are choosen from active list.
        """
        bl_idname = "mbel.assignmat"
        bl_label = "Assign Materials"
        
        def execute(self, context):
                
                mats=bpy.data.materials
                mbe_list = context.scene.mbe_current_list
                matter=[]   #material's list
                
                for m in mats :
                        if m.mbe == mbe_list :
                                matter.append(m)
                
                N=len(matter)    #n. of material
                if N < 1 :
                        self.report({'ERROR'}, "No materials found")
                        return{'CANCELLED'}
                i=0 #counter
                #assign materials to objects...
                for obj in context.selected_objects:                       #for every object in selection
                        if obj.type == 'MESH' :                                  #if it's a mesh
                                i+=0
                                bpy.context.scene.objects.active = obj             #makes it active
                                
                                for mat in obj.material_slots:
                                        bpy.ops.object.material_slot_remove()             #remove all materials
                                
                                bpy.ops.object.material_slot_add()                    #add ONE material
                                obj.data.materials[0]=matter[random.randint(0,N-1)]   #assign one of the N material
                
                self.report({'INFO'}, mbe_list+" list applyied to "+str(N)+" objects")
                
                return{'FINISHED'}


class OBJECT_OT_viztoolDisplayBox(bpy.types.Operator):
        """
        Change selected object's visualization to Box
        """
        bl_idname = "viztool.displaybox"
        bl_label = "Display: Box"
        
        def execute(self, context):
                objs = bpy.context.selected_objects
                for o in objs:
                        o.draw_type = 'BOUNDS'
                self.report({'INFO'}, "Switched to box")
                return{'FINISHED'}


class OBJECT_OT_viztoolDisplayTextured(bpy.types.Operator):
        """
        Change selected object's visualization to Textured
        """
        bl_idname = "viztool.displaytextured"
        bl_label = "Display: Textured"
        
        def execute(self, context):
                objs = bpy.context.selected_objects
                for o in objs:
                        o.draw_type = 'TEXTURED'
                self.report({'INFO'}, "Switched to Textured")
                return{'FINISHED'}



class OBJECT_OT_mbelPurgeMat(bpy.types.Operator):
        """
        Remove unused materials.
        """
        bl_idname = "mbel.purgemat"
        bl_label = "Delete unused materials"
        
        def execute(self, context):
                mats=bpy.data.materials        
                for m in mats :
                        if m.users == 0 :   #if no user found
                                bpy.data.materials.remove(m)   #remove mat
                return{'FINISHED'}

class OBJECT_OT_mbelPurgeText(bpy.types.Operator):
        """
        Remove unused textures.
        """
        bl_idname = "mbel.purgetext"
        bl_label = "Delete unused materials"
        
        def execute(self, context):
                textures=bpy.data.textures        
                for t in textures :
                        if t.users == 0 :   #if no user found
                                bpy.data.textures.remove(t)   #remove mat
                return{'FINISHED'}                         

class OBJECT_OT_mbelSelectOrphans(bpy.types.Operator):
        """
        Select objects with no material applyed
        """
        bl_idname = "mbel.selectorphans"
        bl_label = "Select objects with no material"
        
        def execute(self, context):
                
                i=0 #counter
                for obj in bpy.data.objects :
                        if (obj.type=='MESH') and (len(obj.material_slots)==0) :
                                obj.select=True
                                i+=1

                self.report({'INFO'}, str(i)+" objects selected")
                return{'FINISHED'}

class OBJECT_OT_mbelClearSlot(bpy.types.Operator):
        """
        Clear material's slots of active object.
        """
        bl_idname = "mbel.clearslot"
        bl_label = "Clear material slots"
        
        def execute(self, context):
                
                #checking wether active object is a mesh
                for obj in context.selected_objects :
                        if (obj.type=='MESH') :
                                context.scene.objects.active = obj
                                for i in obj.material_slots :
                                        bpy.ops.object.material_slot_remove()
                
                return{'FINISHED'}

class OBJECT_OT_mbelSeparate(bpy.types.Operator):
        """
        Separate active object into linked polygons.
        """
        bl_idname = "mbel.separate"
        bl_label = "Separate"

        def execute(self, context):
                
                #checking wether active object is a mesh
                if bpy.context.active_object.type != 'MESH' :
                        self.report({'ERROR'}, "Works with MESH only")
                        return{'CANCELLED'}
                
                if bpy.context.mode != 'EDIT':            #if not in edit mode
                        bpy.ops.object.editmode_toggle()      #enters in edit mode
                        bpy.ops.mesh.separate(type='LOOSE')   #separate it by loose parts
                        bpy.ops.object.editmode_toggle()      #exit edit mode
                else :                                    #else
                        bpy.ops.mesh.separate(type='LOOSE')   #separate it by loose parts
                
                self.report({'INFO'}, "Mesh separated")
                return{'FINISHED'}


'''
    createCameraFromView
'''
class OBJECT_OT_viztool_createCameraFromView(bpy.types.Operator) :
    """
    Create camera from current view
    """
    bl_idname = "viztool.createcamerafromview"
    bl_label = "Camera from view"
    
    def execute(self, context) :

        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0), layers=bpy.context.scene.layers[:])
        bpy.ops.view3d.camera_to_view()

        return{'FINISHED'} 
    
    
'''
    createTargetCamera
'''

import bpy

class OBJECT_OT_viztool_createTargetCamera(bpy.types.Operator) :
    """
    Create camera from current view
    """
    bl_idname = "viztool.createtargetcamera"
    bl_label = "Camera from view"
    
    def execute(self, context) :

        if (len(bpy.context.selected_objects) != 0) :
            selected = bpy.context.active_object
            bpy.ops.view3d.snap_cursor_to_selected()

        bpy.ops.object.camera_add(view_align=False, enter_editmode=False, location=(0,0,0), rotation=(0,0,0), layers=bpy.context.scene.layers[:])
        bpy.ops.view3d.camera_to_view()
        camera = bpy.context.active_object;
        
        bpy.ops.object.add(type = 'EMPTY', view_align=False, enter_editmode=False, location=bpy.context.scene.cursor_location, rotation=(0,0,0), layers=bpy.context.scene.layers[:])
        bpy.ops.object.select_pattern(pattern=camera.name, extend=True)   
        
        bpy.ops.object.track_set(type='TRACKTO')
        
        return{'FINISHED'} 
