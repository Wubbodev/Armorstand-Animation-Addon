bl_info = {
    "name": "Armorstand Animator",
    "blender": (3, 6, 0),
    "category": "Object",
}

import bpy
import os
import math
from bpy_extras.io_utils import ExportHelper

#armorstand insert button
class InsertArmorstand(bpy.types.Operator):
    #info about the button
    """Insert 3D Model Of Armorstand Into Project"""
    bl_idname = "object.insert_stand"
    bl_label = "Insert Armorstand"
    bl_options = {'REGISTER', 'UNDO'}
    
    #when button is clicked
    def execute(self, context):
        #import armorstand into project
        bpy.ops.import_scene.fbx(filepath = os.path.dirname(__file__) + '/armorstand.fbx')

        #for some reason objects rotation in the fbx file change to 0.000009 or something
        #so I set all the rotations to 0
        for obj in bpy.context.selected_objects:
            obj.rotation_euler.x = 0

        return {'FINISHED'}

#export the animation into animc file
class ExportArmorstandAnim(bpy.types.Operator, ExportHelper):
    #info about the button
    """Export Animation To animc File"""
    bl_idname = "object.export_stand"
    bl_label = "Export Animation"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".animc"
    #when button is clicked
    def execute(self, context):
        #start editing the file
        transformMetrix = open(self.filepath,'w')

        #write needed things in the file
        transformMetrix.write('interpolate\n')
        transformMetrix.write('length ' + str(bpy.context.scene.frame_end)+'\n')

        #for loop for each frame in the animation
        for f in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
            bpy.context.scene.frame_set(f)

            #frame number
            transformMetrix.write('frame ' + str(f)+'\n')

            #for every selected object (should select all of the armorstand)
            for obj in bpy.context.selected_objects:

                x = obj.rotation_euler.x * 180 / math.pi * -1
                y = obj.rotation_euler.y * 180 / math.pi
                z = obj.rotation_euler.z * 180 / math.pi * -1


                #postion of armorstand needs 4 values
                if obj.name == "Armorstand_Position":
                    transformMetrix.write(obj.name + ' ' + str(obj.location.x) +' '+str(obj.location.y) +' '+str(obj.location.z)+' '+str(z) +'\n')
                #write the rest of the selected objects rotations
                else:    
                    transformMetrix.write(obj.name + ' ' + str(y) +' '+str(z) +' '+str(x)+'\n')

        #stop editing the file
        transformMetrix.close()    

        return {'FINISHED'}      


    
#blender stuff
def insertarm_menu_func(self, context):
    self.layout.operator(InsertArmorstand.bl_idname)

def exportanim_menu_func(self, context):
    self.layout.operator(ExportArmorstandAnim.bl_idname)

#registering and unregistering the classes
def register():
    bpy.utils.register_class(InsertArmorstand)
    bpy.utils.register_class(ExportArmorstandAnim)
    bpy.types.VIEW3D_MT_add.append(insertarm_menu_func)
    bpy.types.VIEW3D_MT_add.append(exportanim_menu_func)

def unregister():
    bpy.utils.unregister_class(InsertArmorstand) 
    bpy.utils.unregister_class(ExportArmorstandAnim)
    
if __name__ == "__main__":
    register()

