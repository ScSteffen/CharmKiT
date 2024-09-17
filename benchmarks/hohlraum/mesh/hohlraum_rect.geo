cl_fine = 0.005;
cl_coarse =cl_fine;
cl_outer = 2.0*cl_fine;
cl_red = 0.5*cl_fine;

upper_left_red = 0.4;
lower_left_red = -0.4;
upper_right_red = 0.4;
lower_right_red = -0.4;
horizontal_left_red = -0.6;
horizontal_right_red = 0.6;

capsule_x = 0.0;
capsule_y = 0.0;


// Outer points
Point(1) = {-0.65, -0.65, 0, cl_coarse};
Point(2) = {0.65, -0.65, 0, cl_coarse};
Point(3) = {-0.65, 0.65, 0, cl_coarse};
Point(4) = {0.65, 0.65, 0, cl_coarse};
//+
Line(1) = {3, 1};
//+
Line(2) = {1, 2};
//+
Line(3) = {2, 4};
//+
Line(4) = {4, 3};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Physical Curve(5) = {1, 2, 3, 4};
//+
Transfinite Surface {1};
Recombine Surface "*";