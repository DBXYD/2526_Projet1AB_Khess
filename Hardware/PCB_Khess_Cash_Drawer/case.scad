/* [Rendering options] */
// Show placeholder PCB in OpenSCAD preview
show_pcb = false;
// Lid mounting method
lid_model = "cap"; // [cap, inner-fit]
// Conditional rendering
render = "case"; // [all, case, lid]


/* [Dimensions] */
// Height of the PCB mounting stand-offs between the bottom of the case and the PCB
standoff_height = 5;
// PCB thickness
pcb_thickness = 1.6;
// Bottom layer thickness
floor_height = 1.2;
// Case wall thickness
wall_thickness = 1.2;
// Space between the top of the PCB and the top of the case
headroom = 5.08;

/* [M2.5 screws] */
// Outer diameter for the insert
insert_M2_5_diameter = 3.27;
// Depth of the insert
insert_M2_5_depth = 3.75;

/* [Hidden] */
$fa=$preview ? 10 : 4;
$fs=0.2;
inner_height = floor_height + standoff_height + pcb_thickness + headroom;

module wall (thickness, height) {
    linear_extrude(height, convexity=10) {
        difference() {
            offset(r=thickness)
                children();
            children();
        }
    }
}

module bottom(thickness, height) {
    linear_extrude(height, convexity=3) {
        offset(r=thickness)
            children();
    }
}

module lid(thickness, height, edge) {
    linear_extrude(height, convexity=10) {
        offset(r=thickness)
            children();
    }
    translate([0,0,-edge])
    difference() {
        linear_extrude(edge, convexity=10) {
                offset(r=-0.2)
                children();
        }
        translate([0,0, -0.5])
         linear_extrude(edge+1, convexity=10) {
                offset(r=-1.2)
                children();
        }
    }
}


module box(wall_thick, bottom_layers, height) {
    if (render == "all" || render == "case") {
        translate([0,0, bottom_layers])
            wall(wall_thick, height) children();
        bottom(wall_thick, bottom_layers) children();
    }
    
    if (render == "all" || render == "lid") {
        translate([0, 0, height+bottom_layers+0.1])
        lid(wall_thick, bottom_layers, lid_model == "inner-fit" ? headroom-2.5: bottom_layers) 
            children();
    }
}

module mount(drill, space, height) {
    translate([0,0,height/2])
        difference() {
            cylinder(h=height, r=(space/2), center=true);
            cylinder(h=(height*2), r=(drill/2), center=true);
            
            translate([0, 0, height/2+0.01])
                children();
        }
        
}

module connector(min_x, min_y, max_x, max_y, height) {
    size_x = max_x - min_x;
    size_y = max_y - min_y;
    translate([(min_x + max_x)/2, (min_y + max_y)/2, height/2])
        cube([size_x, size_y, height], center=true);
}

module Cutout_Pinheader_substract(width, height) {
    translate([0, 0, height/2+0.1])
        cube([10, width+0.2, height+0.2], center=true);
}
module pcb() {
    thickness = 1.6;

    color("#009900")
    difference() {
        linear_extrude(thickness) {
            polygon(points = [[194,86.1], [193.97844,86.64922], [193.91383,87.19501], [193.80659,87.73415], [193.65742,88.26313999999999], [193.46716,88.77875999999999], [193.23707,89.27793], [192.96848,89.7575], [192.66314,90.21453], [192.32287,90.64614999999999], [191.94977,91.04977], [191.54615,91.42286999999999], [191.11453,91.76313999999999], [190.6575,92.06848], [190.17793,92.33707], [189.67876,92.56716], [189.16314,92.75742], [188.63415,92.90659], [188.09501,93.01383], [187.54922,93.07844], [187,93.1], [80,93.1], [79.45078,93.07844], [78.90499,93.01383], [78.36585,92.90659], [77.83686,92.75742], [77.32124,92.56716], [76.82207,92.33707], [76.3425,92.06848], [75.88547,91.76313999999999], [75.45385,91.42286999999999], [75.05023,91.04977], [74.67713,90.64614999999999], [74.33686,90.21453], [74.03152,89.7575], [73.76293,89.27793], [73.53284,88.77875999999999], [73.34258,88.26313999999999], [73.19341,87.73415], [73.08617,87.19501], [73.02156,86.64922], [73,86.1], [73,40], [73.02156,39.45078], [73.08617,38.90499], [73.19341,38.36585], [73.34258,37.83686], [73.53284,37.32124], [73.76293,36.82207], [74.03152,36.3425], [74.33686,35.88547], [74.67713,35.45385], [75.05023,35.05023], [75.45385,34.67713], [75.88547,34.33686], [76.3425,34.03152], [76.82207,33.76293], [77.32124,33.53284], [77.83686,33.34258], [78.36585,33.19341], [78.90499,33.08617], [79.45078,33.02156], [80,33], [187,33], [187.54922,33.02156], [188.09501,33.08617], [188.63415,33.19341], [189.16314,33.34258], [189.67876,33.53284], [190.17793,33.76293], [190.6575,34.03152], [191.11453,34.33686], [191.54615,34.67713], [191.94977,35.05023], [192.32287,35.45385], [192.66314,35.88547], [192.96848,36.3425], [193.23707,36.82207], [193.46716,37.32124], [193.65742,37.83686], [193.80659,38.36585], [193.91383,38.90499], [193.97844,39.45078], [194,40], [194,86.1]]);
        }
    translate([80, 86.1, -1])
        cylinder(thickness+2, 1.3499999999999943, 1.3499999999999943);
    translate([187, 40, -1])
        cylinder(thickness+2, 1.3500000000000014, 1.3500000000000014);
    translate([80, 40, -1])
        cylinder(thickness+2, 1.3500000000000014, 1.3500000000000014);
    translate([187, 86.1, -1])
        cylinder(thickness+2, 1.3499999999999943, 1.3499999999999943);
    }
}

module case_outline() {
    polygon(points = [[195,86], [194.97536,86.62768], [194.90152,87.25144], [194.77896,87.8676], [194.60848,88.47216], [194.39104,89.06144], [194.12808,89.63192], [193.82112,90.18], [193.47216,90.70232], [193.08328,91.1956], [192.65688,91.65688], [192.1956,92.08328], [191.70232,92.47216], [191.18,92.82112], [190.63192,93.12808], [190.06144,93.39104], [189.47216,93.60848], [188.8676,93.77896], [188.25144,93.90152], [187.62768,93.97536], [187,94], [80,94], [79.37232,93.97536], [78.74856,93.90152], [78.1324,93.77896], [77.52784,93.60848], [76.93856,93.39104], [76.36808,93.12808], [75.82,92.82112], [75.29768,92.47216], [74.8044,92.08328], [74.34312,91.65688], [73.91672,91.1956], [73.52784,90.70232], [73.17888,90.18], [72.87192,89.63192], [72.60896,89.06144], [72.39152,88.47216], [72.22104,87.8676], [72.09848,87.25144], [72.02464,86.62768], [72,86], [72,40], [72.02464,39.37232], [72.09848,38.74856], [72.22104,38.1324], [72.39152,37.52784], [72.60896,36.93856], [72.87192,36.36808], [73.17888,35.82], [73.52784,35.29768], [73.91672,34.8044], [74.34312,34.34312], [74.8044,33.91672], [75.29768,33.52784], [75.82,33.17888], [76.36808,32.87192], [76.93856,32.608959999999996], [77.52784,32.39152], [78.1324,32.22104], [78.74856,32.09848], [79.37232,32.02464], [80,32], [187,32], [187.62768,32.02464], [188.25144,32.09848], [188.8676,32.22104], [189.47216,32.39152], [190.06144,32.608959999999996], [190.63192,32.87192], [191.18,33.17888], [191.70232,33.52784], [192.1956,33.91672], [192.65688,34.34312], [193.08328,34.8044], [193.47216,35.29768], [193.82112,35.82], [194.12808,36.36808], [194.39104,36.93856], [194.60848,37.52784], [194.77896,38.1324], [194.90152,38.74856], [194.97536,39.37232], [195,40], [195,86]]);
}

module Insert_M2_5() {
    translate([0, 0, -insert_M2_5_depth])
        cylinder(insert_M2_5_depth, insert_M2_5_diameter/2, insert_M2_5_diameter/2);
    translate([0, 0, -0.3])
        cylinder(0.3, insert_M2_5_diameter/2, insert_M2_5_diameter/2+0.3);
}

rotate([render == "lid" ? 180 : 0, 0, 0])
scale([1, -1, 1])
translate([-133.5, -63.0, 0]) {
    pcb_top = floor_height + standoff_height + pcb_thickness;

    difference() {
        box(wall_thickness, floor_height, inner_height) {
            case_outline();
        }

    // Substract: Unknown
    translate([127.5, 92.3, pcb_top])
    rotate([0, 0, -90])
        Cutout_Pinheader_substract(width=7.62, height=2.54);

    // Substract: Unknown
    translate([112.8, 92.2, pcb_top])
    rotate([0, 0, -90])
        Cutout_Pinheader_substract(width=5.08, height=2.54);

    // Substract: Unknown
    translate([75.1, 51.6, pcb_top])
        Cutout_Pinheader_substract(width=10.16, height=5.08);

    }

    if (show_pcb && $preview) {
        translate([0, 0, floor_height + standoff_height])
            pcb();
    }

    if (render == "all" || render == "case") {
        // H2 [('M2.5', 2.5)]
        translate([80, 86.1, floor_height])
        mount(2.7, 5.9, standoff_height)
            Insert_M2_5();
        // H3 [('M2.5', 2.5)]
        translate([187, 40, floor_height])
        mount(2.7, 5.9, standoff_height)
            Insert_M2_5();
        // H1 [('M2.5', 2.5)]
        translate([80, 40, floor_height])
        mount(2.7, 5.9, standoff_height)
            Insert_M2_5();
        // H4 [('M2.5', 2.5)]
        translate([187, 86.1, floor_height])
        mount(2.7, 5.9, standoff_height)
            Insert_M2_5();
    }
}
