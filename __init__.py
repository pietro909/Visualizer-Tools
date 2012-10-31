'''
    __init__.py
    
'''

bl_info = {
    'name': 'Visualizer Tools',
    'author': 'Pietro Grandi',
    'version': (0, 9, 8 ),
    'blender': (2, 6, 4),
    "location": "View3D > UI panel > Visualizer Tools",
    'description': 'Tools for material editing and use.',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    "category": "Material"
    }
    
import bpy
from bpy.props import (EnumProperty, StringProperty)

if "bpy" in locals() :
    from . import materials         #setup: sets up the environment
    from . import operators
    
    
def setup() :   #, mbe_materials
  
    try :
        t = bpy.context.scene.mbe_current_list
        print(" current list found...")
    except:
        print(" no valid current list found: setting up...")
        
        bpy.types.Scene.mbe_current_list = StringProperty(
        name='mbe_current_list',
        default='default list',
        attr='default list'
        )
    
    try :
        t = bpy.data.materials[0].mbe
        print(" mbe prop found...")
    except:
        print(" no valid mbe prop found: setting up...")
        
        #every material has a new property : the list to which belongs
        bpy.types.Material.mbe = StringProperty(
            name="Material List",
            default='default list',
            attr='default list'
            )
            
    return{'FINISHED'}

setup()

    
#class Menu: menu can be updated dynamically
class BranchMenu(bpy.types.Menu):
    bl_idname = "viztool.branchmenu"
    bl_label = bpy.context.scene.mbe_current_list

    def draw(self, context):
        
        mbe_list = materials.mbeLists()
        layout = self.layout
        
        for m in mbe_list :
            layout.operator('viztool.choosemenu', text = str(m)).name=str(m)
            
            
# MAIN PANEL
class OBJECT_PT_MaterialByElement(bpy.types.Panel) :
    bl_label = "Visualizer Tools "
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"    
        
    def draw(self,context) :
        scene = bpy.context.scene
        layout = self.layout

        #camera tools
        box = layout.box()
        row = box.row()
        row.label("Create camera from view:")
        row = box.row(align=True)
        row.operator('viztool.createcamerafromview', text = "Free")
        row.operator('viztool.createtargetcamera', text = "Targeted")
        
        #objects tool
        box = layout.box()
        row = box.row()
        row.label("Selected objects to:")
        row = box.row(align=True)
        row.operator('viztool.displaybox', text = "Box")
        row.operator('viztool.displaytextured', text = "Textured")
        #material slots tools
        box = layout.box()
        col = box.column()
        row = col.row()
        row.label("Remove unused:")
        row = col.row(align=True)
        row.operator('mbel.purgemat', text = "Materials")
        row.operator('mbel.purgetext', text = "Textures")
        col = box.column(align=True)
        row = col.row(align=True)

        row.operator('mbel.selectorphans', text = "Select orphans")
        
        
        #material's list tools
        box = layout.box()
        row = box.row()
        row.menu('viztool.branchmenu')
        row = box.row()
        row.label(text="Working list: "+context.scene.mbe_current_list)
        
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('mbel.assignmat', text = "Assign to selected")
        row = col.row(align=True)
        row.operator('mbel.selmatted', text = "Select objects")
        row = col.row(align=True)
        row.operator('mbel.separate', text = "Separate subobjects")
        
        col = box.column(align=True)
        row = col.row()
        row.label(text = "Assign to:")
        row = col.row(align=True)
        row.operator('mbel.assigntosubobj', text = "Subobjects")
        row.operator('mbel.assignpolys', text = "Polys")

        col = box.column(align=True)
        row = col.row(align=True)
        #row.operator('mbel.delmatone', text = "Rem Material")   NOT WORKING
        row.operator('mbel.fillslot', text = "Fill slots")
        row.operator('mbel.clearslot', text = "Clear slots")
        
        #material's function
        box = layout.box()
        row = box.row()
        #this is to avoid menu disappearing when you drop off all materials
        if (len(context.active_object.material_slots.items()) > 0) and (context.active_object.material_slots[0].name != '') :
            row.prop(context.active_object.active_material, 'mbe', text="List")
        else :
            row.label("NO MATERIAL FOUND")
        

      
#    Registration

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
