height = 0.2;
outerRadius = 2;


width = 240;
length = 270;

hoopRadius = 4.1;
hoopLengthOffset = 25;
hoopWidthOffset = 36;
hoopEdgeOffset = 6;


pierceRadius = 4;
pierceWidthCount = 10;
pierceLengthCount = 6;
pierceLengthOffset = 39;
pierceWidthOffset = 34.5;

pierceWidthGap = 19;
pierceLengthGap = 20;


$fn = 256;

module basePlate() {
    hull() {
        // front left
        translate([outerRadius, outerRadius, 0])
        cylinder(r=outerRadius, h=height);

        // back left
        translate([outerRadius, length - outerRadius, 0])
        cylinder(r=outerRadius, h=height);


        // front right
        translate([width - outerRadius, outerRadius, 0])
        cylinder(r=outerRadius, h=height);

        // back right
        translate([width - outerRadius, length - outerRadius, 0])
        cylinder(r=outerRadius, h=height);
    }
}

module hoopHoles() {
    // left front
    translate([hoopEdgeOffset, hoopLengthOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([-20, 0, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }


    // left back
    translate([hoopEdgeOffset, length - hoopLengthOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([-20, 0, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }


    // right front
    translate([width - hoopEdgeOffset, hoopLengthOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([+20, 0, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }
    
    // right back
    translate([width - hoopEdgeOffset, length - hoopLengthOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([+20, 0, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }



    // back left
    translate([hoopWidthOffset, length - hoopEdgeOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([0, +20, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }

    // back right
    translate([width - hoopWidthOffset, length - hoopEdgeOffset, -height/2]) {
        hull() {
            cylinder(r=hoopRadius, h=height*2);
            translate([0, +20, 0])
            cylinder(r=hoopRadius, h=height*2);
        }
    }
}

module pierceHoles() {
    widthGap = (width - (pierceWidthOffset * 2)) / (pierceWidthCount - 1);
    lengthGap = pierceLengthGap;
    translate([pierceWidthOffset, pierceLengthOffset, -height/2]) {
        for(column = [0 : pierceLengthCount - 1]) {
            for(row = [0 : pierceWidthCount - 1]) {
                translate([widthGap * row, lengthGap * column, 0])
                cylinder(r=pierceRadius, h=height*2);
            }
        }
    }
}

projection(cut = false) {
    difference() {
        basePlate();
        hoopHoles();
        pierceHoles();
    }
}


// reference
//#cube([width,length,height]);