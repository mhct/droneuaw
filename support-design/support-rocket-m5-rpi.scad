
module holefixer() {
    //produces a holefixer (with space for a 3 mm screw)
    // it has 13 mm heigh
    // the center of the hole is at x=12,y=12
    difference() {
    union() {
        tickness = 3;
        cube([12, 10, tickness], center=true);
        translate([0,0,-15]) cylinder(h=16, r=3, center=false, $fn=100);            
    }    
            translate([0,0,-20]) cylinder(h=30, r=2, center=false, $fn=100);
            
        }

}

module bridge(covered = false) {
    color([1,1,1],1) {
        translate([0,0,0]) rotate([0,-90,0]) union() {
            cube([37, 24, 3]);
            translate([0,6,0]) cube([15, 12, 5]);
        }
        
        translate([76,0,0]) rotate([0,-90,0]) union() {
            cube([37, 24, 3]);
            translate([0,6,-2]) cube([15, 12, 5]);
        }
        if (covered == true) {
            translate([-3, 0, 37]) cube([79,24,3]);    
        }
    }
}

$fn=100;
difference() {
    union() {
        tickness = 3;
        cube([73, 107, tickness]);
        //translate([0,13,0]) bridge(true);
        //translate([0,60,0]) bridge(true);
        
        translate([-6,40,1.5]) holefixer();
        translate([-2,35,1.5]) cube([6, 10, 3], center=false);  //support to make outside wings stronger
        translate([79,40,1.5]) holefixer();
        translate([69,35,1.5]) cube([6, 10, 3], center=false); //support to make outside wings stronger
        

       translate([31.5, 44, 0]) cube([10, 4, 10], center=false);
       translate([26.5, 103, 0]) cube([20, 4, 10], center=false);
       translate([66, 74.5, 0]) cube([4, 10, 10], center=false);
    }


   translate([5.5, 7.5, 0])  cylinder(h=16, r=1.6, center=true);
   translate([14.1, -1, -1])  cube([18,16,7], center=false); // hole for ethernet card 
   translate([64, 50, -1])  cube([6,18,7], center=false); //hole for firmware pins

   translate([66.3, 7.5, 0]) cylinder(h=16, r=1.6, center=true);

   translate([37, 75, 0]) cylinder(h=16, r=24, center=true);
//   translate([37, 20, 0]) cylinder(h=16, r=16, center=true);

}

translate([0,160,0]) rotate([90,0,0]) bridge(true);
translate([10,130,24]) rotate([-90,0,0]) bridge(true);

module measureCheck() {
    color([1.0,0,0], 1) {
        rotate([0,90,0]) cylinder(h=85, r=1, center=false);
    }
}

//translate([-6,40,0]) measureCheck();