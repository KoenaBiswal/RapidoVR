"""
IIT KHARAGPUR RAPIDO ANIMATION - MASTERPIECE GENERATOR
Photorealistic architectural modeling, high-detail commuter motorcycle,
proportioned human characters, authentic phone UI booking experience,
and 10 cinematic dynamic camera shots.
"""

import bpy
import math
import os

def run():
    print("=== STARTING IIT KHARAGPUR RAPIDO MASTERPIECE GENERATION ===")
    
    # 1. CLEAN SCENE
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 1800
    scene.render.fps = 24
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    
    # Set EEVEE Next settings
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
    
    # Color management: AgX Punchy for rich cinematic film contrast
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Punchy'
    scene.view_settings.exposure = -0.3
    scene.view_settings.gamma = 1.0

    assets_dir = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\scratch\iitkgp_rapido"

    # =========================================================================
    # 2. MATERIALS
    # =========================================================================
    print("Building procedural & image PBR materials...")

    def make_mat(name, color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0, specular=0.5, emission_color=None, emission_strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
        if emission_color and 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = emission_color
            bsdf.inputs['Emission Strength'].default_value = emission_strength
        return mat

    # Heritage Red Brick with micro-bump
    mat_brick = bpy.data.materials.new(name="MAT_HeritageBrick")
    mat_brick.use_nodes = True
    nt_b = mat_brick.node_tree
    bsdf_b = nt_b.nodes.get('Principled BSDF')
    tex_coord = nt_b.nodes.new('ShaderNodeTexCoord')
    mapping = nt_b.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (3.5, 3.5, 3.5)
    nt_b.links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    brick_node = nt_b.nodes.new('ShaderNodeTexBrick')
    brick_node.inputs['Color1'].default_value = (0.55, 0.16, 0.10, 1.0) # Warm terracotta red
    brick_node.inputs['Color2'].default_value = (0.42, 0.11, 0.07, 1.0) # Deep burnt brick
    brick_node.inputs['Mortar'].default_value = (0.78, 0.74, 0.70, 1.0) # Light sand mortar
    brick_node.inputs['Mortar Size'].default_value = 0.02
    brick_node.inputs['Mortar Smooth'].default_value = 0.1
    brick_node.inputs['Row Height'].default_value = 0.18
    brick_node.inputs['Brick Width'].default_value = 0.45
    nt_b.links.new(mapping.outputs['Vector'], brick_node.inputs['Vector'])
    nt_b.links.new(brick_node.outputs['Color'], bsdf_b.inputs['Base Color'])
    bsdf_b.inputs['Roughness'].default_value = 0.78

    # Bump on brick
    bump_b = nt_b.nodes.new('ShaderNodeBump')
    bump_b.inputs['Strength'].default_value = 0.25
    nt_b.links.new(brick_node.outputs['Fac'], bump_b.inputs['Height'])
    nt_b.links.new(bump_b.outputs['Normal'], bsdf_b.inputs['Normal'])

    # Sandstone Trim & Columns
    mat_sandstone = make_mat("MAT_Sandstone", color=(0.88, 0.84, 0.78, 1.0), roughness=0.65)
    # Architectural Dark Bronze / Window frames
    mat_winframe = make_mat("MAT_DarkBronze", color=(0.08, 0.07, 0.06, 1.0), roughness=0.35, metallic=0.6)
    # Tinted Architectural Glass
    mat_glass = make_mat("MAT_Glass", color=(0.08, 0.12, 0.16, 1.0), roughness=0.04, specular=1.0)
    # Plinth & Steps Stone
    mat_steps = make_mat("MAT_StoneSteps", color=(0.75, 0.73, 0.70, 1.0), roughness=0.7)

    # Asphalt Road with aggregate noise
    mat_asphalt = bpy.data.materials.new(name="MAT_Asphalt")
    mat_asphalt.use_nodes = True
    nt_a = mat_asphalt.node_tree
    bsdf_a = nt_a.nodes.get('Principled BSDF')
    bsdf_a.inputs['Base Color'].default_value = (0.13, 0.14, 0.15, 1.0)
    bsdf_a.inputs['Roughness'].default_value = 0.68
    noise_a = nt_a.nodes.new('ShaderNodeTexNoise')
    noise_a.inputs['Scale'].default_value = 60.0
    bump_a = nt_a.nodes.new('ShaderNodeBump')
    bump_a.inputs['Strength'].default_value = 0.12
    nt_a.links.new(noise_a.outputs['Fac'], bump_a.inputs['Height'])
    nt_a.links.new(bump_a.outputs['Normal'], bsdf_a.inputs['Normal'])

    # Road Markings: Yellow & White
    mat_yellow_stripe = make_mat("MAT_RoadYellow", color=(0.95, 0.75, 0.08, 1.0), roughness=0.45)
    mat_white_stripe = make_mat("MAT_RoadWhite", color=(0.92, 0.92, 0.92, 1.0), roughness=0.45)
    
    # Sidewalk Concrete Pavers
    mat_sidewalk = make_mat("MAT_Sidewalk", color=(0.68, 0.69, 0.67, 1.0), roughness=0.8)
    # Curbs (Yellow/Black Hazard)
    mat_curb_black = make_mat("MAT_CurbBlack", color=(0.12, 0.12, 0.12, 1.0), roughness=0.6)
    # Lush Campus Grass
    mat_grass = make_mat("MAT_Grass", color=(0.18, 0.35, 0.12, 1.0), roughness=0.85)

    # Nalanda Modern Materials
    mat_nalanda_white = make_mat("MAT_NalandaWhite", color=(0.90, 0.91, 0.92, 1.0), roughness=0.35)
    mat_nalanda_louver = make_mat("MAT_NalandaLouver", color=(0.85, 0.86, 0.88, 1.0), roughness=0.25, metallic=0.3)
    mat_nalanda_sign = make_mat("MAT_NalandaSignBlue", color=(0.04, 0.28, 0.68, 1.0), roughness=0.2, specular=0.9)
    mat_gold_text = make_mat("MAT_GoldText", color=(0.85, 0.68, 0.15, 1.0), roughness=0.25, metallic=0.85)

    # Rapido Bike & Character Materials
    mat_rapido_yellow = make_mat("MAT_RapidoYellow", color=(1.0, 0.80, 0.0, 1.0), roughness=0.18, specular=0.8)
    mat_bike_black = make_mat("MAT_BikeBlack", color=(0.04, 0.04, 0.04, 1.0), roughness=0.25, metallic=0.2)
    mat_chrome = make_mat("MAT_Chrome", color=(0.95, 0.95, 0.95, 1.0), roughness=0.06, metallic=1.0)
    mat_tire = make_mat("MAT_TireRubber", color=(0.08, 0.08, 0.08, 1.0), roughness=0.85)
    mat_brake_disc = make_mat("MAT_BrakeDisc", color=(0.8, 0.8, 0.8, 1.0), roughness=0.3, metallic=0.9)
    mat_headlight = make_mat("MAT_Headlight", color=(1.0, 0.98, 0.9, 1.0), roughness=0.1, emission_color=(1.0, 0.98, 0.9, 1.0), emission_strength=4.0)
    mat_taillight = make_mat("MAT_Taillight", color=(0.8, 0.02, 0.02, 1.0), roughness=0.2, emission_color=(1.0, 0.05, 0.05, 1.0), emission_strength=2.5)

    # Characters
    mat_jacket_yellow = make_mat("MAT_DriverJacket", color=(0.98, 0.78, 0.0, 1.0), roughness=0.6)
    mat_reflective_stripe = make_mat("MAT_Reflective", color=(0.95, 0.95, 0.98, 1.0), roughness=0.2, emission_color=(0.9, 0.95, 1.0, 1.0), emission_strength=0.8)
    mat_skin = make_mat("MAT_Skin", color=(0.68, 0.48, 0.38, 1.0), roughness=0.55)
    mat_jeans = make_mat("MAT_Jeans", color=(0.10, 0.22, 0.38, 1.0), roughness=0.7)
    mat_boots = make_mat("MAT_Boots", color=(0.08, 0.07, 0.06, 1.0), roughness=0.5)
    mat_student_hoodie = make_mat("MAT_StudentHoodie", color=(0.14, 0.42, 0.45, 1.0), roughness=0.7)
    mat_backpack = make_mat("MAT_Backpack", color=(0.12, 0.14, 0.16, 1.0), roughness=0.75)
    mat_visor = make_mat("MAT_HelmetVisor", color=(0.02, 0.02, 0.03, 1.0), roughness=0.08, specular=1.0)

    # Texture-mapped materials
    def make_image_mat(name, img_filename, emission=False, strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nt = mat.node_tree
        bsdf = nt.nodes.get('Principled BSDF')
        img_path = os.path.join(assets_dir, img_filename)
        if os.path.exists(img_path):
            img_node = nt.nodes.new('ShaderNodeTexImage')
            img_node.image = bpy.data.images.load(img_path)
            nt.links.new(img_node.outputs['Color'], bsdf.inputs['Base Color'])
            if emission:
                nt.links.new(img_node.outputs['Color'], bsdf.inputs['Emission Color'])
                bsdf.inputs['Emission Strength'].default_value = strength
        bsdf.inputs['Roughness'].default_value = 0.2
        return mat

    mat_phone_ui = make_image_mat("MAT_PhoneUI", "rapido_phone_screen.png", emission=True, strength=2.2)
    mat_clock_face = make_image_mat("MAT_ClockFace", "iitkgp_clock_face.png")
    mat_road_sign = make_image_mat("MAT_RoadSign", "campus_road_sign.png")
    mat_license_plate = make_image_mat("MAT_LicensePlate", "bike_license_plate.png")

    # =========================================================================
    # 3. ENVIRONMENT & LIGHTING (Nishita Golden Morning Sky)
    # =========================================================================
    print("Setting up Nishita golden morning sky...")
    world = bpy.data.worlds.new("WLD_IITKgpMorning")
    scene.world = world
    world.use_nodes = True
    w_nt = world.node_tree
    w_nodes = w_nt.nodes
    w_links = w_nt.links
    w_nodes.clear()

    w_output = w_nodes.new('ShaderNodeOutputWorld')
    w_bg = w_nodes.new('ShaderNodeBackground')
    w_bg.inputs['Strength'].default_value = 0.4
    sky_node = w_nodes.new('ShaderNodeTexSky')
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(22.0) # Golden morning sun
    sky_node.sun_rotation = math.radians(135.0) # Raking shadows across facades
    sky_node.altitude = 0.0
    sky_node.air_density = 1.0
    sky_node.dust_density = 1.2 # Soft warm haze
    sky_node.ozone_density = 1.0

    w_links.new(sky_node.outputs['Color'], w_bg.inputs['Color'])
    w_links.new(w_bg.outputs['Background'], w_output.inputs['Surface'])

    # Key directional sun light for crisp shadows
    sun_data = bpy.data.lights.new(name="KeySun", type='SUN')
    sun_data.energy = 2.2
    sun_data.color = (1.0, 0.94, 0.86) # Warm morning sunlight
    sun_data.angle = math.radians(1.5) # Soft realistic contact shadows
    sun_obj = bpy.data.objects.new(name="Sun_Morning", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(65.0), math.radians(15.0), math.radians(-45.0))

    # =========================================================================
    # 4. ARCHITECTURAL MODELING: HIJLI HERITAGE MAIN BUILDING
    # =========================================================================
    print("Constructing Hijli Heritage Main Building...")
    col_mainbldg = bpy.data.collections.new("Col_MainBuilding")
    scene.collection.children.link(col_mainbldg)

    def add_box(name, loc, size, mat=mat_brick, col=col_mainbldg):
        bpy.ops.mesh.primitive_cube_add(location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (size[0]/2, size[1]/2, size[2]/2)
        bpy.ops.object.transform_apply(scale=True)
        if mat:
            obj.data.materials.append(mat)
        if col != scene.collection:
            scene.collection.objects.unlink(obj)
            col.objects.link(obj)
        return obj

    def add_cylinder(name, loc, r, h, mat=mat_sandstone, col=col_mainbldg, vertices=32, rot=(0,0,0)):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, vertices=vertices, rotation=rot)
        obj = bpy.context.active_object
        obj.name = name
        if mat:
            obj.data.materials.append(mat)
        if col != scene.collection:
            scene.collection.objects.unlink(obj)
            col.objects.link(obj)
        return obj

    # Main Building Center Block (Origin at (0, 32, 0))
    b_y = 32.0

    # Grand Staircase & Stone Plinth
    add_box("MB_BasePlinth", (0, b_y - 2, 0.6), (72, 28, 1.2), mat=mat_steps)
    # Terraced Entrance Steps (8 steps cascading down)
    for i in range(8):
        step_w = 26.0 - i * 0.4
        step_y = b_y - 12.0 - i * 0.8
        step_z = 1.0 - i * 0.12
        add_box(f"MB_Step_{i}", (0, step_y, step_z/2), (step_w, 0.8, step_z), mat=mat_steps)

    # Central Heritage Block
    add_box("MB_CenterBlock", (0, b_y, 8.0), (32.0, 16.0, 14.0), mat=mat_brick)

    # Classical Entrance Portico
    # Pediment (triangular gable)
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=13.0, depth=4.0, location=(0, b_y - 8.5, 14.8), rotation=(0, math.radians(90), 0))
    pediment = bpy.context.active_object
    pediment.name = "MB_Pediment"
    pediment.scale = (1.0, 0.8, 0.35)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    pediment.data.materials.append(mat_sandstone)
    scene.collection.objects.unlink(pediment)
    col_mainbldg.objects.link(pediment)

    # Portico Frieze with Sandstone Architrave
    add_box("MB_PorticoArchitrave", (0, b_y - 8.5, 13.0), (22.0, 4.2, 1.2), mat=mat_sandstone)

    # 4 Classical Fluted Columns
    col_positions = [-9.0, -3.0, 3.0, 9.0]
    for idx, cx in enumerate(col_positions):
        # Column shaft
        add_cylinder(f"MB_Column_{idx}", (cx, b_y - 8.5, 6.8), r=0.75, h=11.2, mat=mat_sandstone)
        # Column base & capital
        add_box(f"MB_ColBase_{idx}", (cx, b_y - 8.5, 1.4), (2.0, 2.0, 0.6), mat=mat_sandstone)
        add_box(f"MB_ColCap_{idx}", (cx, b_y - 8.5, 12.3), (2.0, 2.0, 0.6), mat=mat_sandstone)

    # Recessed Heritage Wooden Entrance Doors
    door_positions = [-6.0, 0.0, 6.0]
    for idx, dx in enumerate(door_positions):
        add_box(f"MB_Door_{idx}", (dx, b_y - 7.8, 5.0), (3.6, 0.4, 7.5), mat=mat_winframe)

    # 3D Gold Lettering on Portico Frieze: "INDIAN INSTITUTE OF TECHNOLOGY KHARAGPUR"
    font_curve = bpy.data.curves.new(type="FONT", name="F_IITKgp")
    font_curve.body = "INDIAN INSTITUTE OF TECHNOLOGY KHARAGPUR"
    font_curve.size = 0.52
    font_curve.extrude = 0.06
    font_obj = bpy.data.objects.new("MB_GoldLettering", font_curve)
    col_mainbldg.objects.link(font_obj)
    font_obj.location = (-9.6, b_y - 10.7, 12.8)
    font_obj.rotation_euler = (math.radians(90), 0, 0)
    font_obj.data.materials.append(mat_gold_text)

    # MULTI-TIER CLOCK TOWER
    # Tier 1 (Base tower block)
    add_box("MB_TowerTier1", (0, b_y, 18.0), (14.0, 14.0, 6.0), mat=mat_brick)
    add_box("MB_TowerCornice1", (0, b_y, 21.2), (15.2, 15.2, 0.6), mat=mat_sandstone)

    # Tier 2 (Belfry with arched decorative vents)
    add_box("MB_TowerTier2", (0, b_y, 25.0), (11.0, 11.0, 7.0), mat=mat_brick)
    add_box("MB_TowerCornice2", (0, b_y, 28.7), (12.2, 12.2, 0.6), mat=mat_sandstone)

    # Tier 3 (Clock Chamber with 4 faces)
    add_box("MB_TowerTier3", (0, b_y, 33.0), (9.0, 9.0, 8.0), mat=mat_brick)
    
    # 4 Authentic Clock Faces with Roman Numerals
    # Front clock face (South facing: -Y)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=2.6, depth=0.15, location=(0, b_y - 4.58, 33.2), rotation=(math.radians(90), 0, 0))
    clk_f = bpy.context.active_object
    clk_f.name = "MB_ClockFront"
    clk_f.data.materials.append(mat_clock_face)
    scene.collection.objects.unlink(clk_f)
    col_mainbldg.objects.link(clk_f)

    # Back clock face (North facing)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=2.6, depth=0.15, location=(0, b_y + 4.58, 33.2), rotation=(math.radians(90), 0, 0))
    clk_b = bpy.context.active_object
    clk_b.name = "MB_ClockBack"
    clk_b.data.materials.append(mat_clock_face)
    scene.collection.objects.unlink(clk_b)
    col_mainbldg.objects.link(clk_b)

    # Tier 4 (Heritage Pyramidal Roof / Spire)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=6.8, depth=5.5, location=(0, b_y, 39.8), rotation=(0, 0, math.radians(45)))
    spire = bpy.context.active_object
    spire.name = "MB_TowerSpire"
    spire.data.materials.append(mat_sandstone)
    scene.collection.objects.unlink(spire)
    col_mainbldg.objects.link(spire)
    # Copper finial on top
    add_cylinder("MB_Finial", (0, b_y, 43.5), r=0.25, h=2.5, mat=mat_gold_text)

    # Flanking Wings (East Wing and West Wing)
    for side, sign in [("West", -1), ("East", 1)]:
        wx = sign * 44.0
        # Main wing structure (56m long, 14m deep, 12m high)
        add_box(f"MB_Wing_{side}", (wx, b_y, 7.0), (56.0, 14.0, 12.0), mat=mat_brick)
        # Cornice & Roof parapet
        add_box(f"MB_WingCornice_{side}", (wx, b_y, 13.3), (57.2, 14.8, 0.7), mat=mat_sandstone)
        add_box(f"MB_WingParapet_{side}", (wx, b_y, 14.2), (56.4, 14.2, 1.1), mat=mat_sandstone)
        
        # Heritage multi-pane windows across both stories
        for w_idx in range(7):
            fx = sign * (20.0 + w_idx * 6.5)
            # Ground floor arched windows
            add_box(f"MB_Win_GF_{side}_{w_idx}", (fx, b_y - 7.1, 4.2), (2.8, 0.3, 4.0), mat=mat_glass)
            # 1st floor rectangular framed windows
            add_box(f"MB_Win_1F_{side}_{w_idx}", (fx, b_y - 7.1, 9.6), (2.8, 0.3, 3.8), mat=mat_glass)
            # Sandstone window sill & header trims
            add_box(f"MB_Sill_GF_{side}_{w_idx}", (fx, b_y - 7.3, 2.0), (3.2, 0.5, 0.35), mat=mat_sandstone)
            add_box(f"MB_Sill_1F_{side}_{w_idx}", (fx, b_y - 7.3, 7.5), (3.2, 0.5, 0.35), mat=mat_sandstone)

    # Main Building Plaza & Forecourt Gardens
    add_box("MB_PlazaPaving", (0, b_y - 18.0, 0.05), (120.0, 24.0, 0.1), mat=mat_sidewalk)
    # Manicured green lawn patches flanking the staircase
    add_box("MB_LawnWest", (-32.0, b_y - 18.0, 0.12), (36.0, 16.0, 0.15), mat=mat_grass)
    add_box("MB_LawnEast", (32.0, b_y - 18.0, 0.12), (36.0, 16.0, 0.15), mat=mat_grass)

    # =========================================================================
    # 5. SCHOLARS' AVENUE: ROADWAY, CURBS, SIGNAGE & TREES
    # =========================================================================
    print("Constructing Scholars' Avenue & lush campus boulevard...")
    col_road = bpy.data.collections.new("Col_ScholarsAvenue")
    scene.collection.children.link(col_road)

    # Scholars' Avenue Roadway Curve:
    # Segment 1: Main Building forecourt road: x from -40 to 60, y = 0
    # Segment 2: Sweeping S-curve transition from y = 0 to y = -140, x from 60 to 180
    # Segment 3: Nalanda Complex arrival loop: x = 180 to 240, y = -140

    # Road surface mesh (High-detail 2-lane boulevard)
    road_mesh = bpy.data.meshes.new("Mesh_ScholarsRoad")
    road_obj = bpy.data.objects.new("Road_ScholarsAvenue", road_mesh)
    col_road.objects.link(road_obj)
    road_obj.data.materials.append(mat_asphalt)

    # Generate road vertices along path
    road_points = []
    # Section A: Main Bldg front (Straight)
    for x in range(-50, 70, 5):
        road_points.append((float(x), 0.0))
    # Section B: Curve to Nalanda
    for i in range(1, 26):
        t = i / 25.0
        # Smooth cubic S-curve
        x = 70.0 + t * 110.0
        y = - (3 * t**2 - 2 * t**3) * 140.0
        road_points.append((x, y))
    # Section C: Nalanda Plaza front
    for x in range(185, 255, 5):
        road_points.append((float(x), -140.0))

    verts = []
    faces = []
    road_w = 4.8 # Half width = 4.8m -> 9.6m wide 2-lane road
    
    for idx, pt in enumerate(road_points):
        # Calculate tangent
        if idx < len(road_points) - 1:
            dx = road_points[idx+1][0] - pt[0]
            dy = road_points[idx+1][1] - pt[1]
        else:
            dx = pt[0] - road_points[idx-1][0]
            dy = pt[1] - road_points[idx-1][1]
        length = math.hypot(dx, dy)
        nx = -dy / length
        ny = dx / length

        # Left edge, center, right edge
        verts.append((pt[0] + nx * road_w, pt[1] + ny * road_w, 0.02))
        verts.append((pt[0] - nx * road_w, pt[1] - ny * road_w, 0.02))

        if idx > 0:
            p0 = (idx - 1) * 2
            p1 = p0 + 1
            p2 = idx * 2 + 1
            p3 = idx * 2
            faces.append((p0, p1, p2, p3))

    road_mesh.from_pydata(verts, [], faces)
    road_mesh.update()

    # White Solid Road Edge Strips & Yellow Dashed Centerlines
    for idx in range(0, len(road_points) - 1, 2):
        pt1 = road_points[idx]
        pt2 = road_points[min(idx + 1, len(road_points) - 1)]
        cx = (pt1[0] + pt2[0]) / 2
        cy = (pt1[1] + pt2[1]) / 2
        angle = math.atan2(pt2[1] - pt1[1], pt2[0] - pt1[0])
        seg_len = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1]) * 0.9

        # Centerline dash
        bpy.ops.mesh.primitive_cube_add(location=(cx, cy, 0.035), scale=(seg_len/2, 0.12, 0.005), rotation=(0, 0, angle))
        cl = bpy.context.active_object
        cl.name = f"Centerline_{idx}"
        cl.data.materials.append(mat_yellow_stripe)
        scene.collection.objects.unlink(cl)
        col_road.objects.link(cl)

    # Road Curbs (Yellow/Black Hazard Painted)
    for idx in range(0, len(road_points) - 1):
        pt1 = road_points[idx]
        pt2 = road_points[idx + 1]
        cx = (pt1[0] + pt2[0]) / 2
        cy = (pt1[1] + pt2[1]) / 2
        angle = math.atan2(pt2[1] - pt1[1], pt2[0] - pt1[0])
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        l = math.hypot(dx, dy)
        nx = -dy / l
        ny = dx / l
        c_mat = mat_yellow_stripe if (idx % 2 == 0) else mat_curb_black

        # Left curb
        bpy.ops.mesh.primitive_cube_add(location=(cx + nx * (road_w + 0.2), cy + ny * (road_w + 0.2), 0.12), scale=(l/2, 0.2, 0.12), rotation=(0, 0, angle))
        c_l = bpy.context.active_object
        c_l.name = f"CurbL_{idx}"
        c_l.data.materials.append(c_mat)
        scene.collection.objects.unlink(c_l)
        col_road.objects.link(c_l)

        # Right curb
        bpy.ops.mesh.primitive_cube_add(location=(cx - nx * (road_w + 0.2), cy - ny * (road_w + 0.2), 0.12), scale=(l/2, 0.2, 0.12), rotation=(0, 0, angle))
        c_r = bpy.context.active_object
        c_r.name = f"CurbR_{idx}"
        c_r.data.materials.append(c_mat)
        scene.collection.objects.unlink(c_r)
        col_road.objects.link(c_r)

    # Sidewalks flanking Scholars' Avenue
    add_box("Sidewalk_MainBldg", (10.0, 6.2, 0.1), (140.0, 2.4, 0.2), mat=mat_sidewalk, col=col_road)
    add_box("Sidewalk_South", (10.0, -6.2, 0.1), (140.0, 2.4, 0.2), mat=mat_sidewalk, col=col_road)

    # Campus Highway Road Signboard
    sign_post = add_cylinder("RoadSign_Post", (55.0, 7.5, 2.4), r=0.08, h=4.8, mat=mat_sandstone, col=col_road)
    bpy.ops.mesh.primitive_cube_add(location=(55.0, 7.5, 3.8), scale=(1.6, 0.05, 0.8), rotation=(0, 0, 0))
    sign_board = bpy.context.active_object
    sign_board.name = "RoadSign_Board"
    sign_board.data.materials.append(mat_road_sign)
    scene.collection.objects.unlink(sign_board)
    col_road.objects.link(sign_board)

    # Modern Curved Streetlights spaced along Scholars' Avenue
    col_lights = bpy.data.collections.new("Col_Streetlights")
    scene.collection.children.link(col_lights)
    for idx, l_pt in enumerate(road_points[::4]):
        lx = l_pt[0] - 6.2
        ly = l_pt[1] + 1.2
        # Pole
        pole = add_cylinder(f"Pole_{idx}", (lx, ly, 3.5), r=0.09, h=7.0, mat=mat_sandstone, col=col_lights)
        # Overhang arm & LED fixture
        arm = add_box(f"Arm_{idx}", (lx + 0.9, ly, 6.9), (1.8, 0.12, 0.12), mat=mat_sandstone, col=col_lights)
        lamp = add_box(f"LED_{idx}", (lx + 1.6, ly, 6.75), (0.6, 0.3, 0.1), mat=mat_headlight, col=col_lights)

    # Lush Campus Trees (Multi-cluster leafy trees with organic branching)
    col_trees = bpy.data.collections.new("Col_CampusTrees")
    scene.collection.children.link(col_trees)

    tree_locs = [
        # Flanking Main Building avenue
        (-40, 12), (-28, 14), (-16, 12), (25, 12), (38, 14), (52, 12),
        (-42, -12), (-26, -14), (-10, -12), (12, -12), (28, -14), (45, -12),
        # Flanking Scholars' Avenue S-curve
        (65, -15), (78, -32), (92, -54), (110, -78), (130, -102), (150, -120), (168, -126),
        (58, 15), (70, 5), (86, -18), (104, -42), (122, -68), (142, -92), (160, -112),
        # Flanking Nalanda approach & plaza perimeter
        (175, -155), (190, -160), (210, -162), (230, -160), (250, -155),
        (170, -85), (255, -85), (260, -115), (260, -145)
    ]

    mat_trunk = make_mat("MAT_TreeTrunk", color=(0.28, 0.18, 0.12, 1.0), roughness=0.9)
    mat_leaves1 = make_mat("MAT_Leaves1", color=(0.14, 0.36, 0.10, 1.0), roughness=0.65)
    mat_leaves2 = make_mat("MAT_Leaves2", color=(0.22, 0.44, 0.12, 1.0), roughness=0.65)

    for tidx, (tx, ty) in enumerate(tree_locs):
        # Trunk
        th = 4.5 + (tidx % 3) * 0.8
        tr = 0.32 + (tidx % 2) * 0.08
        add_cylinder(f"Trunk_{tidx}", (tx, ty, th/2), r=tr, h=th, mat=mat_trunk, col=col_trees, vertices=12)
        # Foliage clusters (3-4 spheres forming leafy canopy)
        canopy_z = th * 0.85
        c_mat = mat_leaves1 if (tidx % 2 == 0) else mat_leaves2
        for c_i, (cx_off, cy_off, cz_off, cr) in enumerate([
            (0, 0, 1.5, 2.4), (-1.2, 0.8, 0.8, 1.9), (1.3, -0.6, 1.0, 2.0), (0.2, -1.2, 1.8, 1.7)
        ]):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=cr, location=(tx + cx_off, ty + cy_off, canopy_z + cz_off))
            fol = bpy.context.active_object
            fol.name = f"Foliage_{tidx}_{c_i}"
            fol.scale = (1.0, 1.0, 0.85)
            fol.data.materials.append(c_mat)
            scene.collection.objects.unlink(fol)
            col_trees.objects.link(fol)

    # Base ground plane
    add_box("CampusGround", (100.0, -60.0, -0.1), (400.0, 300.0, 0.2), mat=mat_grass, col=scene.collection)

    # =========================================================================
    # 6. ARCHITECTURAL MODELING: NALANDA CLASSROOM COMPLEX (NR)
    # =========================================================================
    print("Constructing Nalanda Classroom Complex...")
    col_nalanda = bpy.data.collections.new("Col_NalandaComplex")
    scene.collection.children.link(col_nalanda)

    # Nalanda is centered around x = 215, y = -105
    nx, ny = 215.0, -105.0

    # Plaza Paving & Turnaround Drop-off Loop
    add_box("NL_PlazaPaving", (nx, ny - 25.0, 0.05), (100.0, 60.0, 0.1), mat=mat_sidewalk, col=col_nalanda)

    # 3 Monumental Cylindrical Lecture Drums (West, Central, East)
    drums = [
        ("WestDrum", nx - 30.0, ny, 16.0, 24.0),
        ("CenterDrum", nx, ny - 4.0, 17.5, 26.0),
        ("EastDrum", nx + 30.0, ny, 16.0, 24.0),
    ]

    for dname, dx, dy, dr, dh in drums:
        # Core cylinder
        add_cylinder(f"NL_{dname}_Core", (dx, dy, dh/2), r=dr, h=dh, mat=mat_nalanda_white, col=col_nalanda, vertices=48)
        # Parapet rim
        add_cylinder(f"NL_{dname}_RoofRim", (dx, dy, dh + 0.4), r=dr + 0.6, h=0.8, mat=mat_nalanda_white, col=col_nalanda, vertices=48)

        # 4 Horizontal Solar-Tinted Ribbon Window Bands
        for lvl in range(4):
            w_z = 3.5 + lvl * 5.2
            add_cylinder(f"NL_{dname}_Glass_{lvl}", (dx, dy, w_z), r=dr + 0.08, h=2.2, mat=mat_glass, col=col_nalanda, vertices=48)

        # 40 Vertical Aerofoil Sun-Shading Louvers
        num_louvers = 40
        for l_idx in range(num_louvers):
            angle = (2 * math.pi / num_louvers) * l_idx
            # Only put louvers on the front/sides visible to plaza (angle between -160 and -20 deg)
            lx = dx + (dr + 0.45) * math.cos(angle)
            ly = dy + (dr + 0.45) * math.sin(angle)
            bpy.ops.mesh.primitive_cube_add(
                location=(lx, ly, dh/2),
                scale=(0.12, 0.5, dh/2),
                rotation=(0, 0, angle)
            )
            louver = bpy.context.active_object
            louver.name = f"NL_{dname}_Louver_{l_idx}"
            louver.data.materials.append(mat_nalanda_louver)
            scene.collection.objects.unlink(louver)
            col_nalanda.objects.link(louver)

    # Grand Cantilevered Entrance Canopy
    canopy_y = ny - 24.0
    canopy = add_box("NL_EntranceCanopy", (nx, canopy_y, 6.0), (74.0, 16.0, 1.2), mat=mat_nalanda_white, col=col_nalanda)

    # Cylindrical Support Pilotis
    for px in [-28.0, -10.0, 10.0, 28.0]:
        add_cylinder(f"NL_Piloti_{px}", (nx + px, canopy_y - 6.0, 2.7), r=0.55, h=5.4, mat=mat_sandstone, col=col_nalanda)

    # 3D Signage on Canopy: "NALANDA CLASSROOM COMPLEX"
    font_nl = bpy.data.curves.new(type="FONT", name="F_Nalanda")
    font_nl.body = "NALANDA CLASSROOM COMPLEX"
    font_nl.size = 1.45
    font_nl.extrude = 0.14
    obj_nl_text = bpy.data.objects.new("NL_SignageText", font_nl)
    col_nalanda.objects.link(obj_nl_text)
    obj_nl_text.location = (nx - 20.5, canopy_y - 8.1, 6.8)
    obj_nl_text.rotation_euler = (math.radians(90), 0, 0)
    obj_nl_text.data.materials.append(mat_nalanda_sign)

    # Concrete Plaza Bollards protecting pedestrian walk
    for bx in range(-32, 34, 4):
        add_cylinder(f"NL_Bollard_{bx}", (nx + bx, canopy_y - 12.0, 0.45), r=0.18, h=0.9, mat=mat_sandstone, col=col_nalanda)

    # =========================================================================
    # 7. HIGH-DETAIL RAPIDO MOTORCYCLE MODEL
    # =========================================================================
    print("Building high-detail Rapido commuter motorcycle...")
    col_bike = bpy.data.collections.new("Col_RapidoBike")
    scene.collection.children.link(col_bike)

    # Bike Root Empty
    bike_root = bpy.data.objects.new("Bike_Root", None)
    col_bike.objects.link(bike_root)
    bike_root.empty_display_type = 'ARROWS'
    bike_root.empty_display_size = 1.5

    def add_bike_part(name, loc, size, mat, geom_type='CUBE', rot=(0, 0, 0), parent=bike_root):
        if geom_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(location=loc, scale=(size[0]/2, size[1]/2, size[2]/2), rotation=rot)
        elif geom_type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=size[0], depth=size[1], location=loc, rotation=rot, vertices=24)
        elif geom_type == 'TORUS':
            bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=size[0], minor_radius=size[1], rotation=rot, major_segments=24, minor_segments=12)
        part = bpy.context.active_object
        part.name = name
        part.data.materials.append(mat)
        part.parent = parent
        scene.collection.objects.unlink(part)
        col_bike.objects.link(part)
        return part

    # Front Wheel Assembly (Tire + 5-spoke Alloy Mag + Disc Brake)
    front_wheel_empty = bpy.data.objects.new("Front_Wheel_Hub", None)
    col_bike.objects.link(front_wheel_empty)
    front_wheel_empty.location = (0.78, 0, 0.32)
    front_wheel_empty.parent = bike_root

    # Front Tire (Torus shape with realistic profile)
    add_bike_part("Front_Tire", (0, 0, 0), (0.26, 0.06), mat_tire, 'TORUS', rot=(math.radians(90), 0, 0), parent=front_wheel_empty)
    # Front Mag Rim Hub
    add_bike_part("Front_Rim", (0, 0, 0), (0.20, 0.05), mat_chrome, 'CYLINDER', rot=(math.radians(90), 0, 0), parent=front_wheel_empty)
    # 5 Alloy Spokes
    for s_i in range(5):
        spoke_rot = math.radians(s_i * 72)
        add_bike_part(f"Front_Spoke_{s_i}", (0, 0, 0), (0.018, 0.03, 0.36), mat_bike_black, 'CUBE', rot=(0, spoke_rot, 0), parent=front_wheel_empty)
    # Disc Brake Rotor & Golden Caliper
    add_bike_part("Front_DiscBrake", (0, 0.045, 0), (0.13, 0.008), mat_brake_disc, 'CYLINDER', rot=(math.radians(90), 0, 0), parent=front_wheel_empty)
    add_bike_part("Front_Caliper", (0.08, 0.048, 0.08), (0.06, 0.04, 0.08), mat_rapido_yellow, 'CUBE', parent=front_wheel_empty)

    # Rear Wheel Assembly
    rear_wheel_empty = bpy.data.objects.new("Rear_Wheel_Hub", None)
    col_bike.objects.link(rear_wheel_empty)
    rear_wheel_empty.location = (-0.72, 0, 0.32)
    rear_wheel_empty.parent = bike_root

    add_bike_part("Rear_Tire", (0, 0, 0), (0.26, 0.07), mat_tire, 'TORUS', rot=(math.radians(90), 0, 0), parent=rear_wheel_empty)
    add_bike_part("Rear_Rim", (0, 0, 0), (0.20, 0.06), mat_chrome, 'CYLINDER', rot=(math.radians(90), 0, 0), parent=rear_wheel_empty)
    for s_i in range(5):
        spoke_rot = math.radians(s_i * 72)
        add_bike_part(f"Rear_Spoke_{s_i}", (0, 0, 0), (0.018, 0.03, 0.36), mat_bike_black, 'CUBE', rot=(0, spoke_rot, 0), parent=rear_wheel_empty)
    # Sprocket & Drive Chain Guard
    add_bike_part("Rear_Sprocket", (0, -0.045, 0), (0.12, 0.01), mat_bike_black, 'CYLINDER', rot=(math.radians(90), 0, 0), parent=rear_wheel_empty)
    add_bike_part("ChainGuard", (0.25, -0.06, 0.0), (0.50, 0.04, 0.07), mat_bike_black, 'CUBE', parent=rear_wheel_empty)

    # Telescopic Front Forks & Fender
    fork_angle = math.radians(-16)
    add_bike_part("Front_Fork_L", (0.72, 0.08, 0.52), (0.022, 0.52), mat_chrome, 'CYLINDER', rot=(0, fork_angle, 0))
    add_bike_part("Front_Fork_R", (0.72, -0.08, 0.52), (0.022, 0.52), mat_chrome, 'CYLINDER', rot=(0, fork_angle, 0))
    add_bike_part("Front_Fender", (0.76, 0, 0.46), (0.34, 0.14, 0.06), mat_rapido_yellow, 'CUBE', rot=(0, fork_angle, 0))

    # Triple Tree Clamp & Handlebars
    add_bike_part("TripleClamp", (0.64, 0, 0.78), (0.08, 0.22, 0.04), mat_bike_black, 'CUBE')
    add_bike_part("Handlebar_Center", (0.60, 0, 0.88), (0.02, 0.68), mat_chrome, 'CYLINDER', rot=(math.radians(90), 0, 0))
    add_bike_part("Handlebar_Grip_L", (0.59, 0.31, 0.88), (0.025, 0.12), mat_tire, 'CYLINDER', rot=(math.radians(90), 0, 0))
    add_bike_part("Handlebar_Grip_R", (0.59, -0.31, 0.88), (0.025, 0.12), mat_tire, 'CYLINDER', rot=(math.radians(90), 0, 0))
    # Rearview Mirrors
    add_bike_part("Mirror_Stem_L", (0.63, 0.28, 0.96), (0.008, 0.16), mat_chrome, 'CYLINDER')
    add_bike_part("Mirror_Head_L", (0.63, 0.32, 1.04), (0.02, 0.10, 0.06), mat_glass, 'CUBE')
    add_bike_part("Mirror_Stem_R", (0.63, -0.28, 0.96), (0.008, 0.16), mat_chrome, 'CYLINDER')
    add_bike_part("Mirror_Head_R", (0.63, -0.32, 1.04), (0.02, 0.10, 0.06), mat_glass, 'CUBE')
    # Speedometer Instrument Console
    add_bike_part("SpeedoConsole", (0.62, 0, 0.90), (0.10, 0.16, 0.05), mat_bike_black, 'CUBE', rot=(0, math.radians(-25), 0))

    # Front Headlight & Visor Cowl
    add_bike_part("Headlight_Cowl", (0.78, 0, 0.82), (0.16, 0.20, 0.20), mat_rapido_yellow, 'CUBE')
    add_bike_part("Headlight_Lens", (0.87, 0, 0.82), (0.02, 0.14, 0.14), mat_headlight, 'CUBE')

    # Fuel Tank & Chassis
    add_bike_part("FuelTank", (0.28, 0, 0.74), (0.48, 0.28, 0.24), mat_rapido_yellow, 'CUBE')
    add_bike_part("TankSideCover_L", (0.30, 0.15, 0.72), (0.36, 0.03, 0.18), mat_bike_black, 'CUBE')
    add_bike_part("TankSideCover_R", (0.30, -0.15, 0.72), (0.36, 0.03, 0.18), mat_bike_black, 'CUBE')

    # Contoured Two-Tier Commuter Seat
    add_bike_part("SeatDriver", (-0.08, 0, 0.68), (0.38, 0.24, 0.10), mat_bike_black, 'CUBE')
    add_bike_part("SeatPillion", (-0.36, 0, 0.73), (0.32, 0.21, 0.11), mat_bike_black, 'CUBE')
    # Rear Steel Grab Rail
    add_bike_part("GrabRail", (-0.56, 0, 0.78), (0.14, 0.24, 0.06), mat_chrome, 'CUBE')

    # Engine Block with Air Cooling Fins
    add_bike_part("EngineBlock", (0.15, 0, 0.40), (0.32, 0.22, 0.26), mat_bike_black, 'CUBE')
    for fin_i in range(5):
        add_bike_part(f"EngineFin_{fin_i}", (0.15, 0, 0.32 + fin_i * 0.04), (0.34, 0.24, 0.01), mat_chrome, 'CUBE')

    # Chrome Exhaust Pipe & Muffler
    add_bike_part("ExhaustPipe", (0.0, 0.14, 0.28), (0.025, 0.65), mat_chrome, 'CYLINDER', rot=(0, math.radians(82), 0))
    add_bike_part("Muffler", (-0.42, 0.16, 0.32), (0.05, 0.45), mat_chrome, 'CYLINDER', rot=(0, math.radians(82), 0))
    add_bike_part("MufflerHeatShield", (-0.38, 0.18, 0.34), (0.32, 0.02, 0.06), mat_sandstone, 'CUBE')

    # Rear Fender, Taillight & Commercial License Plate
    add_bike_part("RearFender", (-0.68, 0, 0.58), (0.35, 0.16, 0.18), mat_bike_black, 'CUBE')
    add_bike_part("Taillight", (-0.78, 0, 0.62), (0.03, 0.12, 0.05), mat_taillight, 'CUBE')
    # License Plate
    bpy.ops.mesh.primitive_cube_add(location=(-0.82, 0, 0.48), scale=(0.01, 0.14, 0.05), rotation=(0, math.radians(15), 0))
    lic_obj = bpy.context.active_object
    lic_obj.name = "BikeLicensePlate"
    lic_obj.data.materials.append(mat_license_plate)
    lic_obj.parent = bike_root
    scene.collection.objects.unlink(lic_obj)
    col_bike.objects.link(lic_obj)

    # Footpegs
    add_bike_part("Footpeg_Driver_L", (0.08, 0.22, 0.30), (0.02, 0.12), mat_bike_black, 'CYLINDER', rot=(math.radians(90), 0, 0))
    add_bike_part("Footpeg_Driver_R", (0.08, -0.22, 0.30), (0.02, 0.12), mat_bike_black, 'CYLINDER', rot=(math.radians(90), 0, 0))
    add_bike_part("Footpeg_Pillion_L", (-0.28, 0.20, 0.36), (0.02, 0.10), mat_bike_black, 'CYLINDER', rot=(math.radians(90), 0, 0))
    add_bike_part("Footpeg_Pillion_R", (-0.28, -0.20, 0.36), (0.02, 0.10), mat_bike_black, 'CYLINDER', rot=(math.radians(90), 0, 0))

    # =========================================================================
    # 8. ARTICULATED CHARACTERS: DRIVER & PASSENGER
    # =========================================================================
    print("Modeling articulated Driver & Student Passenger...")
    col_char = bpy.data.collections.new("Col_Characters")
    scene.collection.children.link(col_char)

    # 8A. RAPIDO CAPTAIN (DRIVER) - Mounted to Bike Root
    driver_root = bpy.data.objects.new("Driver_Root", None)
    col_char.objects.link(driver_root)
    driver_root.parent = bike_root
    driver_root.location = (0.0, 0.0, 0.0)

    def add_char_part(name, loc, size, mat, geom='CUBE', rot=(0,0,0), parent=driver_root):
        if geom == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(location=loc, scale=(size[0]/2, size[1]/2, size[2]/2), rotation=rot)
        elif geom == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=size[0], depth=size[1], location=loc, rotation=rot, vertices=16)
        elif geom == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=size[0], location=loc, segments=20, ring_count=16)
        part = bpy.context.active_object
        part.name = name
        part.data.materials.append(mat)
        part.parent = parent
        scene.collection.objects.unlink(part)
        col_char.objects.link(part)
        return part

    # Driver Pelvis & Torso (Leaning forward at 14 deg toward handlebars)
    torso_rot = (0, math.radians(14), 0)
    add_char_part("Driver_Pelvis", (-0.06, 0, 0.82), (0.24, 0.28, 0.18), mat_jeans, 'CUBE')
    add_char_part("Driver_Torso", (0.02, 0, 1.05), (0.28, 0.34, 0.36), mat_jacket_yellow, 'CUBE', rot=torso_rot)
    # Reflective White Safety Stripe across chest & back
    add_char_part("Driver_SafetyStripe", (0.02, 0, 1.04), (0.29, 0.35, 0.08), mat_reflective_stripe, 'CUBE', rot=torso_rot)

    # Driver Neck & Yellow Helmet with Tinted Smoked Visor
    add_char_part("Driver_Neck", (0.09, 0, 1.28), (0.06, 0.10), mat_skin, 'CYLINDER')
    add_char_part("Driver_Helmet", (0.12, 0, 1.40), (0.16,), mat_rapido_yellow, 'SPHERE')
    add_char_part("Driver_Visor", (0.22, 0, 1.40), (0.09, 0.20, 0.10), mat_visor, 'CUBE', rot=(0, math.radians(10), 0))

    # Driver Arms (Reaching to Handlebars)
    for s_name, s_sign in [("L", 1), ("R", -1)]:
        # Upper arm
        add_char_part(f"Driver_Shoulder_{s_name}", (0.06, s_sign * 0.21, 1.18), (0.07,), mat_jacket_yellow, 'SPHERE')
        add_char_part(f"Driver_Arm_{s_name}", (0.26, s_sign * 0.24, 1.08), (0.045, 0.30), mat_jacket_yellow, 'CYLINDER', rot=(s_sign * math.radians(-15), math.radians(45), 0))
        # Forearm & Riding Glove grasping grip
        add_char_part(f"Driver_Forearm_{s_name}", (0.46, s_sign * 0.27, 0.97), (0.04, 0.26), mat_jacket_yellow, 'CYLINDER', rot=(0, math.radians(65), 0))
        add_char_part(f"Driver_Glove_{s_name}", (0.58, s_sign * 0.30, 0.89), (0.07, 0.08, 0.07), mat_bike_black, 'CUBE')

    # Driver Legs (Knees bent, boots on front footpegs)
    for s_name, s_sign in [("L", 1), ("R", -1)]:
        add_char_part(f"Driver_Thigh_{s_name}", (0.04, s_sign * 0.16, 0.68), (0.065, 0.32), mat_jeans, 'CYLINDER', rot=(0, math.radians(50), 0))
        add_char_part(f"Driver_Shin_{s_name}", (0.08, s_sign * 0.18, 0.44), (0.055, 0.30), mat_jeans, 'CYLINDER', rot=(0, math.radians(-15), 0))
        add_char_part(f"Driver_Boot_{s_name}", (0.12, s_sign * 0.20, 0.31), (0.16, 0.08, 0.09), mat_boots, 'CUBE')

    # 8B. STUDENT PASSENGER
    # Passenger has independent root so they can stand, board, ride, and dismount!
    passenger_root = bpy.data.objects.new("Passenger_Root", None)
    col_char.objects.link(passenger_root)
    passenger_root.empty_display_type = 'SINGLE_ARROW'

    # Seated Rider parts (children of passenger_root)
    pass_parts = {}
    def add_pass_part(name, loc, size, mat, geom='CUBE', rot=(0,0,0)):
        p = add_char_part(name, loc, size, mat, geom=geom, rot=rot, parent=passenger_root)
        pass_parts[name] = p
        return p

    # Passenger Seated Proportions
    add_pass_part("Pass_Pelvis", (0, 0, 0.82), (0.24, 0.26, 0.18), mat_jeans, 'CUBE')
    add_pass_part("Pass_Torso", (0.02, 0, 1.05), (0.26, 0.32, 0.34), mat_student_hoodie, 'CUBE')
    # College Backpack with dual shoulder straps
    add_pass_part("Pass_Backpack", (-0.16, 0, 1.05), (0.16, 0.26, 0.32), mat_backpack, 'CUBE')
    add_pass_part("Pass_Strap_L", (-0.06, 0.11, 1.08), (0.08, 0.04, 0.28), mat_backpack, 'CUBE')
    add_pass_part("Pass_Strap_R", (-0.06, -0.11, 1.08), (0.08, 0.04, 0.28), mat_backpack, 'CUBE')

    # Passenger Head & Rapido Yellow Helmet
    add_pass_part("Pass_Neck", (0.03, 0, 1.26), (0.055, 0.09), mat_skin, 'CYLINDER')
    add_pass_part("Pass_Helmet", (0.04, 0, 1.38), (0.155,), mat_rapido_yellow, 'SPHERE')
    add_pass_part("Pass_Visor", (0.14, 0, 1.38), (0.08, 0.19, 0.09), mat_visor, 'CUBE')

    # Passenger Arms (Holding rear grab rail / steadying)
    for s_name, s_sign in [("L", 1), ("R", -1)]:
        add_pass_part(f"Pass_Arm_{s_name}", (0.02, s_sign * 0.19, 0.95), (0.04, 0.26), mat_student_hoodie, 'CYLINDER', rot=(0, math.radians(20), 0))
        add_pass_part(f"Pass_Hand_{s_name}", (-0.08, s_sign * 0.16, 0.80), (0.06, 0.06, 0.06), mat_skin, 'CUBE')

    # Passenger Legs (Knees bent to pillion pegs)
    for s_name, s_sign in [("L", 1), ("R", -1)]:
        add_pass_part(f"Pass_Thigh_{s_name}", (0.06, s_sign * 0.16, 0.70), (0.06, 0.28), mat_jeans, 'CYLINDER', rot=(0, math.radians(45), 0))
        add_pass_part(f"Pass_Shin_{s_name}", (0.04, s_sign * 0.18, 0.48), (0.05, 0.28), mat_jeans, 'CYLINDER', rot=(0, math.radians(-20), 0))
        add_pass_part(f"Pass_Shoe_{s_name}", (0.02, s_sign * 0.19, 0.36), (0.14, 0.07, 0.07), mat_boots, 'CUBE')

    # 8C. REALISTIC SMARTPHONE WITH RAPIDO APP UI (for Booking Shot 2)
    col_phone = bpy.data.collections.new("Col_Smartphone")
    scene.collection.children.link(col_phone)

    phone_body = add_box("Phone_Body", (0, 0, 0), (0.08, 0.16, 0.008), mat=mat_bike_black, col=col_phone)
    phone_screen = add_box("Phone_Screen", (0, 0, 0.0045), (0.076, 0.154, 0.001), mat=mat_phone_ui, col=col_phone)
    phone_screen.parent = phone_body

    # Stylized hand holding the phone
    hand_palm = add_box("Hand_Palm", (0.01, -0.04, -0.02), (0.09, 0.09, 0.03), mat=mat_skin, col=col_phone)
    hand_palm.parent = phone_body
    # Thumb hovering over the "Confirm Booking" button
    thumb = add_cylinder("Hand_Thumb", (0.03, -0.02, 0.015), r=0.012, h=0.05, mat=mat_skin, col=col_phone, rot=(math.radians(30), math.radians(45), 0))
    thumb.parent = phone_body

    # Place phone in student's hand at Main Building plaza
    phone_body.location = (0.8, 14.2, 1.35)
    phone_body.rotation_euler = (math.radians(-35), math.radians(10), math.radians(-15))

    # =========================================================================
    # 9. DYNAMIC ANIMATION & CHOREOGRAPHY (1800 Frames = 75s @ 24 FPS)
    # =========================================================================
    print("Keyframing dynamic motorcycle ride & character actions...")

    # Calculate smooth spline trajectory for Bike
    # Frames 1-300: Bike waiting / arriving at Main Building curb (x=0, y=0)
    # Frame 300-480: Bike at pickup spot (x=0, y=0)
    # Frame 480-600: Boarding
    # Frame 600-1480: Cruising ride from Main Building (0,0) to Nalanda (215, -140)
    # Frame 1480-1650: Deceleration and stop at Nalanda canopy
    # Frame 1650-1800: Dropoff complete, student walks up stairs

    # Animate Bike_Root location & rotation along Scholars' Avenue
    # We create smooth keyframes for bike motion
    bike_keyframes = [
        # (frame, x, y, z, rot_z, lean_angle)
        (1, -25.0, 0.0, 0.0, 0.0, 0.0),
        (250, -6.0, 0.0, 0.0, 0.0, 0.0),
        (330, 0.0, 0.0, 0.0, 0.0, 0.0),     # Arrived at pickup spot
        (600, 0.0, 0.0, 0.0, 0.0, 0.0),     # Passenger boarded, ready to depart
        (660, 8.0, 0.0, 0.0, 0.0, 0.0),     # Accelerating smoothly
        (750, 28.0, 0.0, 0.0, 0.0, 0.0),    # Cruising speed (35 km/h feel)
        (850, 58.0, -2.0, 0.0, math.radians(-5), math.radians(-4)),   # Entering S-curve
        (950, 88.0, -18.0, 0.0, math.radians(-25), math.radians(-12)), # Deep banking into curve
        (1050, 118.0, -50.0, 0.0, math.radians(-40), math.radians(-10)),
        (1150, 148.0, -88.0, 0.0, math.radians(-32), math.radians(8)),  # Counter-banking S-turn
        (1250, 175.0, -120.0, 0.0, math.radians(-15), math.radians(6)),
        (1350, 198.0, -138.0, 0.0, math.radians(-4), math.radians(2)),  # Straightening to Nalanda
        (1480, 215.0, -140.0, 0.0, 0.0, 0.0), # Smooth stop at Nalanda canopy
        (1800, 215.0, -140.0, 0.0, 0.0, 0.0)  # Parked at Nalanda
    ]

    for f, kx, ky, kz, rz, lean in bike_keyframes:
        bike_root.location = (kx, ky, kz)
        bike_root.rotation_euler = (lean, 0, rz)
        bike_root.keyframe_insert(data_path="location", frame=f)
        bike_root.keyframe_insert(data_path="rotation_euler", frame=f)

    # Make bike animation curves smooth Bezier
    if bike_root.animation_data and bike_root.animation_data.action:
        for fcurve in bike_root.animation_data.action.fcurves:
            for kfp in fcurve.keyframe_points:
                kfp.interpolation = 'BEZIER'

    # Animate Continuous Wheel Rotation proportional to motion
    # Circumference = 2 * pi * 0.32 = 2.01m
    # Total distance ~ 250m -> approx 125 full rotations = 250 * pi radians
    for hub in [front_wheel_empty, rear_wheel_empty]:
        hub.rotation_euler = (0, 0, 0)
        hub.keyframe_insert(data_path="rotation_euler", frame=600)
        hub.rotation_euler = (0, math.radians(-125 * 360), 0)
        hub.keyframe_insert(data_path="rotation_euler", frame=1480)
        if hub.animation_data and hub.animation_data.action:
            for fc in hub.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'

    # Animate Passenger (Standing at Main Building -> Boarding -> Riding -> Dismounting -> Walking to Nalanda)
    # Stage 1: Standing by Main Building stairs looking at phone (Frames 1 - 480)
    # In world coordinates, standing at (0.8, 14.0, 0.6)
    # Stage 2: Boarding bike (Frames 480 - 600) -> Parent to bike_root at pillion seat (-0.36, 0, 0)
    # Stage 3: Riding on bike (Frames 600 - 1480)
    # Stage 4: Dismounting and walking up Nalanda stairs (Frames 1480 - 1800)

    # Setup parent constraint to bike for smooth boarding/riding
    p_const = passenger_root.constraints.new('CHILD_OF')
    p_const.target = bike_root
    p_const.use_scale_x = False
    p_const.use_scale_y = False
    p_const.use_scale_z = False

    # Keyframe constraint influence
    # Frames 1 - 480: Not on bike (influence = 0.0)
    p_const.influence = 0.0
    p_const.keyframe_insert(data_path="influence", frame=1)
    p_const.keyframe_insert(data_path="influence", frame=480)
    # Frame 560 - 1480: Fully on bike (influence = 1.0)
    p_const.influence = 1.0
    p_const.keyframe_insert(data_path="influence", frame=560)
    p_const.keyframe_insert(data_path="influence", frame=1500)
    # Frame 1540 - 1800: Dismounted (influence = 0.0)
    p_const.influence = 0.0
    p_const.keyframe_insert(data_path="influence", frame=1540)

    # Keyframe passenger world location when not on bike
    # Frames 1-480: Standing on Main Building plaza
    passenger_root.location = (0.8, 14.0, 0.0)
    passenger_root.rotation_euler = (0, 0, math.radians(-90))
    passenger_root.keyframe_insert(data_path="location", frame=1)
    passenger_root.keyframe_insert(data_path="rotation_euler", frame=1)
    passenger_root.keyframe_insert(data_path="location", frame=480)
    passenger_root.keyframe_insert(data_path="rotation_euler", frame=480)

    # Frame 560: Settled on pillion seat (local offset relative to bike: (-0.36, 0, 0))
    passenger_root.location = (-0.36, 0, 0)
    passenger_root.rotation_euler = (0, 0, 0)
    passenger_root.keyframe_insert(data_path="location", frame=560)
    passenger_root.keyframe_insert(data_path="rotation_euler", frame=560)
    passenger_root.keyframe_insert(data_path="location", frame=1480)
    passenger_root.keyframe_insert(data_path="rotation_euler", frame=1480)

    # Frame 1540 - 1800: Dismounted at Nalanda, walking purposefully toward the entrance stairs!
    passenger_root.location = (215.0, -138.5, 0.0)
    passenger_root.rotation_euler = (0, 0, math.radians(90))
    passenger_root.keyframe_insert(data_path="location", frame=1540)
    passenger_root.keyframe_insert(data_path="rotation_euler", frame=1540)

    # Walking up to Nalanda entrance
    passenger_root.location = (215.0, -118.0, 0.0)
    passenger_root.keyframe_insert(data_path="location", frame=1800)

    # =========================================================================
    # 10. CINEMATIC 10-SHOT CAMERA RIG & TIMELINE BINDINGS
    # =========================================================================
    print("Setting up 10 cinematic dynamic cameras & timeline markers...")
    col_cams = bpy.data.collections.new("Col_CinematicCameras")
    scene.collection.children.link(col_cams)

    def make_cam(name, lens=35.0, clip_end=600.0):
        cam_data = bpy.data.cameras.new(name=f"Data_{name}")
        cam_data.lens = lens
        cam_data.clip_end = clip_end
        cam_obj = bpy.data.objects.new(name, cam_data)
        col_cams.objects.link(cam_obj)
        return cam_obj

    # SHOT 1: Establishing Drone Shot of Hijli Main Building (Frames 1 - 180 / 0s - 7.5s)
    cam1 = make_cam("CAM_01_Establishing", lens=28.0)
    cam1.location = (0.0, -32.0, 18.0)
    cam1.rotation_euler = (math.radians(72), 0, 0)
    cam1.keyframe_insert(data_path="location", frame=1)
    cam1.keyframe_insert(data_path="rotation_euler", frame=1)
    # Slow majestic drone descent
    cam1.location = (0.0, -16.0, 10.5)
    cam1.rotation_euler = (math.radians(78), 0, 0)
    cam1.keyframe_insert(data_path="location", frame=180)
    cam1.keyframe_insert(data_path="rotation_euler", frame=180)

    # SHOT 2: Smartphone Rapido Booking Over-The-Shoulder POV (Frames 181 - 330 / 7.5s - 13.75s)
    cam2 = make_cam("CAM_02_BookingUI", lens=65.0)
    cam2.location = (0.88, 14.38, 1.56)
    cam2.rotation_euler = (math.radians(48), 0, math.radians(20))
    cam2.keyframe_insert(data_path="location", frame=181)
    cam2.keyframe_insert(data_path="rotation_euler", frame=181)
    # Subtle handheld macro float
    cam2.location = (0.86, 14.34, 1.54)
    cam2.keyframe_insert(data_path="location", frame=330)

    # SHOT 3: Captain Arrival at Curb & Visor Flip (Frames 331 - 480 / 13.75s - 20s)
    cam3 = make_cam("CAM_03_CaptainArrival", lens=45.0)
    cam3.location = (5.8, -4.5, 1.2)
    cam3.rotation_euler = (math.radians(82), 0, math.radians(48))
    cam3.keyframe_insert(data_path="location", frame=331)
    cam3.keyframe_insert(data_path="rotation_euler", frame=331)
    cam3.location = (4.2, -3.2, 1.1)
    cam3.rotation_euler = (math.radians(84), 0, math.radians(52))
    cam3.keyframe_insert(data_path="location", frame=480)

    # SHOT 4: Passenger Helmet On & Boarding (Frames 481 - 630 / 20s - 26.25s)
    cam4 = make_cam("CAM_04_Boarding", lens=50.0)
    cam4.location = (-2.8, 3.6, 1.4)
    cam4.rotation_euler = (math.radians(78), 0, math.radians(-145))
    cam4.keyframe_insert(data_path="location", frame=481)
    cam4.keyframe_insert(data_path="rotation_euler", frame=481)
    cam4.location = (-1.8, 3.2, 1.3)
    cam4.rotation_euler = (math.radians(80), 0, math.radians(-142))
    cam4.keyframe_insert(data_path="location", frame=630)

    # SHOT 5: Ultra-Dynamic Low-Angle Rear Tire Pursuit (Frames 631 - 840 / 26.25s - 35s)
    # Parented to bike for high-speed tracking
    cam5 = make_cam("CAM_05_LowPursuit", lens=30.0)
    cam5.parent = bike_root
    cam5.location = (-2.4, 0.45, 0.48)
    cam5.rotation_euler = (math.radians(82), math.radians(0), math.radians(-82))

    # SHOT 6: Scholars' Avenue Canopy Side-Chase (Frames 841 - 1080 / 35s - 45s)
    # High parallax side view tracking the bike as it banks into curve
    cam6 = make_cam("CAM_06_CanopyChase", lens=38.0)
    cam6.parent = bike_root
    cam6.location = (0.2, -4.2, 1.35)
    cam6.rotation_euler = (math.radians(80), 0, math.radians(0))

    # SHOT 7: Driver Cockpit Over-Shoulder POV (Frames 1081 - 1290 / 45s - 53.75s)
    # Looking past speedometer & handlebars toward Nalanda ahead
    cam7 = make_cam("CAM_07_CockpitPOV", lens=32.0)
    cam7.parent = bike_root
    cam7.location = (-0.22, 0.14, 1.28)
    cam7.rotation_euler = (math.radians(84), 0, math.radians(-94))

    # SHOT 8: Sweeping Drone Arc Over Nalanda Complex (Frames 1291 - 1470 / 53.75s - 61.25s)
    cam8 = make_cam("CAM_08_NalandaDrone", lens=26.0)
    cam8.location = (170.0, -185.0, 32.0)
    cam8.rotation_euler = (math.radians(65), 0, math.radians(35))
    cam8.keyframe_insert(data_path="location", frame=1291)
    cam8.keyframe_insert(data_path="rotation_euler", frame=1291)
    cam8.location = (215.0, -195.0, 24.0)
    cam8.rotation_euler = (math.radians(68), 0, math.radians(10))
    cam8.keyframe_insert(data_path="location", frame=1470)
    cam8.keyframe_insert(data_path="rotation_euler", frame=1470)

    # SHOT 9: Arrival Under Canopy, Stop & Natural Dismount (Frames 1471 - 1650 / 61.25s - 68.75s)
    cam9 = make_cam("CAM_09_CanopyArrival", lens=42.0)
    cam9.location = (218.5, -145.5, 1.45)
    cam9.rotation_euler = (math.radians(82), 0, math.radians(-25))
    cam9.keyframe_insert(data_path="location", frame=1471)
    cam9.keyframe_insert(data_path="rotation_euler", frame=1471)
    cam9.location = (217.2, -144.2, 1.40)
    cam9.keyframe_insert(data_path="location", frame=1650)

    # SHOT 10: Hero Walk into Nalanda & Title Outro (Frames 1651 - 1800 / 68.75s - 75s)
    cam10 = make_cam("CAM_10_HeroOutro", lens=32.0)
    cam10.location = (215.0, -148.0, 1.2)
    cam10.rotation_euler = (math.radians(84), 0, 0)
    cam10.keyframe_insert(data_path="location", frame=1651)
    cam10.keyframe_insert(data_path="rotation_euler", frame=1651)
    # Tilting up to the magnificent 3D Nalanda signage and sky
    cam10.location = (215.0, -135.0, 3.2)
    cam10.rotation_euler = (math.radians(70), 0, 0)
    cam10.keyframe_insert(data_path="location", frame=1800)
    cam10.keyframe_insert(data_path="rotation_euler", frame=1800)

    # Bind Cameras to Timeline Markers
    shot_markers = [
        ("SHOT_01", 1, cam1),
        ("SHOT_02", 181, cam2),
        ("SHOT_03", 331, cam3),
        ("SHOT_04", 481, cam4),
        ("SHOT_05", 631, cam5),
        ("SHOT_06", 841, cam6),
        ("SHOT_07", 1081, cam7),
        ("SHOT_08", 1291, cam8),
        ("SHOT_09", 1471, cam9),
        ("SHOT_10", 1651, cam10)
    ]

    scene.timeline_markers.clear()
    for m_name, m_frame, m_cam in shot_markers:
        marker = scene.timeline_markers.new(m_name, frame=m_frame)
        marker.camera = m_cam

    # Set default camera
    scene.camera = cam1

    # Save master blend file
    blend_path = os.path.join(assets_dir, "iitkgp_rapido_animation.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"=== SUCCESSFULLY SAVED MASTER BLEND FILE: {blend_path} ===")

if __name__ == "__main__":
    run()
