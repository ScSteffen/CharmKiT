cl_fine = 0.01;
cl_mid = cl_fine * 2;
cl_coarse = cl_fine * 4;
cl_coarsest = cl_fine * 6;

Point(2) = {3.5, -3.5, 0, cl_coarsest};
Point(4) = {3.5, 3.5, 0, cl_coarsest};

// Inner grid
Point(5) = { 0., -2.5, 0, cl_coarse };
Point(6) = { 0., -1.5, 0, cl_mid };
Point(7) = { 0., -0.5, 0, cl_fine };
Point(8) = { 0., 0.5, 0, cl_fine };
Point(9) = { 0., 1.5, 0, cl_mid };
Point(10) = { 0., 2.5, 0, cl_coarse };

Point(71) = { 0.5, -2.5, 0, cl_coarse };
Point(73) = { 0.5, -1.5, 0, cl_mid };
Point(75) = { 0.5, -0.5, 0, cl_fine };
Point(77) = { 0.5, 0.5, 0, cl_fine };
Point(79) = { 0.5, 1.5, 0, cl_mid };
Point(93) = { 1.5, -2.5, 0, cl_coarse };
Point(95) = { 1.5, -1.5, 0, cl_mid };
Point(97) = { 1.5, -0.5, 0, cl_mid };
Point(99) = { 1.5, 0.5, 0, cl_mid };
Point(101) = { 1.5, 1.5, 0, cl_mid };
Point(103) = { 1.5, 2.5, 0, cl_coarse };
Point(115) = { 2.5, -2.5, 0, cl_coarse };
Point(117) = { 2.5, -1.5, 0, cl_coarse };
Point(119) = { 2.5, -0.5, 0, cl_coarse };
Point(121) = { 2.5, 0.5, 0, cl_coarse };
Point(123) = { 2.5, 1.5, 0, cl_coarse };
Point(125) = { 2.5, 2.5, 0, cl_coarse };

// helper boundary points
Point(131) = { 0.0, -3.5, 0, cl_coarsest };

Point(142) = { 0.0, 3.5, 0, cl_coarsest };


Point(1002) = {-3.5, -3.5, 0, cl_coarsest};
Point(1004) = {-3.5, 3.5, 0, cl_coarsest};

// Inner grid


Point(10071) = {- 0.5, -2.5, 0, cl_coarse };
Point(10073) = {- 0.5, -1.5, 0, cl_mid };
Point(10075) = {- 0.5, -0.5, 0, cl_fine };
Point(10077) = {- 0.5, 0.5, 0, cl_fine };
Point(10079) = {- 0.5, 1.5, 0, cl_mid };
Point(10093) = {- 1.5, -2.5, 0, cl_coarse };
Point(10095) = {- 1.5, -1.5, 0, cl_mid };
Point(10097) = {- 1.5, -0.5, 0, cl_mid };
Point(10099) = {- 1.5, 0.5, 0, cl_mid };
Point(100101) = {- 1.5, 1.5, 0, cl_mid };
Point(100103) = {- 1.5, 2.5, 0, cl_coarse };
Point(100115) = {- 2.5, -2.5, 0, cl_coarse };
Point(100117) = {- 2.5, -1.5, 0, cl_coarse };
Point(100119) = {- 2.5, -0.5, 0, cl_coarse };
Point(100121) = {- 2.5, 0.5, 0, cl_coarse };
Point(100123) = {- 2.5, 1.5, 0, cl_coarse };
Point(100125) = {- 2.5, 2.5, 0, cl_coarse };


// Horizontal and vertical lines in inner grid
//+
Line(26) = {142, 10};
//+
Line(27) = {10, 9};
//+
Line(28) = {9, 8};
//+
Line(29) = {8, 7};
//+
Line(30) = {7, 6};
//+
Line(31) = {6, 5};
//+
Line(32) = {5, 131};
//+


//+
Line(49) = {7, 75};
//+
Line(50) = {75, 77};
//+
Line(51) = {77, 8};
//+
Line(52) = {77, 79};
//+
Line(53) = {79, 101};
//+
Line(54) = {101, 99};
//+
Line(55) = {99, 77};
//+
Line(56) = {75, 73};
//+
Line(57) = {73, 95};
//+
Line(58) = {95, 97};
//+
Line(59) = {97, 75};
//+
Line(60) = {95, 93};
//+
Line(61) = {93, 115};
//+
Line(62) = {115, 117};
//+
Line(63) = {117, 95};
//+
Line(64) = {99, 97};
//+
Line(65) = {97, 119};
//+
Line(66) = {119, 121};
//+
Line(67) = {121, 99};
//+
Line(68) = {101, 123};
//+
Line(69) = {123, 125};
//+
Line(70) = {125, 103};
//+
Line(71) = {103, 101};
//+
Line(72) = {73, 71};
//+
Line(73) = {71, 5};
//+
Line(74) = {6, 73};
//+
Line(79) = {103, 10};
//+
Line(80) = {123, 121};
//+
Line(81) = {119, 117};
//+
Line(82) = {93, 71};
//+
Curve Loop(1) = {73, -31, 74, 72};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {74, -56, -49, 30};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {49, 50, 51, 29};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {57, 58, 59, 56};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {60, 61, 62, 63};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {65, 66, 67, 64};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {55, -50, -59, -64};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {54, 55, 52, 53};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {68, 69, 70, 71};
//+
Plane Surface(9) = {9};
//+
//+

//+
Line(75) = {131, 2};
//+
Line(76) = {2, 4};
//+
Line(77) = {4, 142};
//+
//+
Line(78) = {9, 79};
//+
Curve Loop(11) = {52, -78, 28, -51};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {71, -53, -78, -27, -79};
//+
Plane Surface(13) = {12};
//+
Curve Loop(13) = {80, 67, -54, 68};
//+
Plane Surface(14) = {13};
//+
Curve Loop(14) = {81, 63, 58, 65};
//+
Plane Surface(15) = {14};
//+
Curve Loop(15) = {82, -72, 57, 60};
//+
Plane Surface(16) = {15};
//+
Curve Loop(16) = {75, 76, 77, 26, -79, -70, -69, 80, -66, 81, -62, -61, 82, 73, 32};
//+
Plane Surface(17) = {16};
// ==============================================================================
// Horizontal and vertical lines in inner grid
//+
//+


//+
Line(10049) = {7, 10075};
//+
Line(10050) = {10075, 10077};
//+
Line(10051) = {10077, 8};
//+
Line(10052) = {10077, 10079};
//+
Line(10053) = {10079, 100101};
//+
Line(10054) = {100101, 10099};
//+
Line(10055) = {10099, 10077};
//+
Line(10056) = {10075, 10073};
//+
Line(10057) = {10073, 10095};
//+
Line(10058) = {10095, 10097};
//+
Line(10059) = {10097, 10075};
//+
Line(10060) = {10095, 10093};
//+
Line(10061) = {10093, 100115};
//+
Line(10062) = {100115, 100117};
//+
Line(10063) = {100117, 10095};
//+
Line(10064) = {10099, 10097};
//+
Line(10065) = {10097, 100119};
//+
Line(10066) = {100119, 100121};
//+
Line(10067) = {100121, 10099};
//+
Line(10068) = {100101, 100123};
//+
Line(10069) = {100123, 100125};
//+
Line(10070) = {100125, 100103};
//+
Line(10071) = {100103, 100101};
//+
Line(10072) = {10073, 10071};
//+
Line(10073) = {10071, 5};
//+
Line(10074) = {6, 10073};
//+
Line(10079) = {100103, 10};
//+
Line(10080) = {100123, 100121};
//+
Line(10081) = {100119, 100117};
//+
Line(10082) = {10093, 10071};
//+
Curve Loop(1001) = {10073, -31, 10074, 10072};
//+
Plane Surface(1001) = {1001};
//+
Curve Loop(1002) = {10074, -10056, -10049, 30};
//+
Plane Surface(1002) = {1002};
//+
Curve Loop(1003) = {10049, 10050, 10051, 29};
//+
Plane Surface(1003) = {1003};
//+
Curve Loop(1004) = {10057, 10058, 10059, 10056};
//+
Plane Surface(1004) = {1004};
//+
Curve Loop(1005) = {10060, 10061, 10062, 10063};
//+
Plane Surface(1005) = {1005};
//+
Curve Loop(1006) = {10065, 10066, 10067, 10064};
//+
Plane Surface(1006) = {1006};
//+
Curve Loop(1007) = {10055, -10050, -10059, -10064};
//+
Plane Surface(1007) = {1007};
//+
Curve Loop(1008) = {10054, 10055, 10052, 10053};
//+
Plane Surface(1008) = {1008};
//+
Curve Loop(1009) = {10068, 10069, 10070, 10071};
//+
Plane Surface(1009) = {1009};
//+
//+

//+
Line(10075) = {131, 1002};
//+
Line(10076) = {1002, 1004};
//+
Line(10077) = {1004, 142};
//+
//+
Line(10078) = {9, 10079};
//+
Curve Loop(10011) = {10052, -10078, 28, -10051};
//+
Plane Surface(10011) = {10011};
//+
Curve Loop(10012) = {10071, -10053, -10078, -27, -10079};
//+
Plane Surface(10013) = {10012};
//+
Curve Loop(10013) = {10080, 10067, -10054, 10068};
//+
Plane Surface(10014) = {10013};
//+
Curve Loop(10014) = {10081, 10063, 10058, 10065};
//+
Plane Surface(10015) = {10014};
//+
Curve Loop(10015) = {10082, -10072, 10057, 10060};
//+
Plane Surface(10016) = {10015};
//+
Curve Loop(10016) = {10075,10076, 10077, 26, -10079, -10070, -10069, 10080, -10066, 10081, -10062, -10061, 10082, 10073, 32};
//+
Plane Surface(10017) = {10016};
// ==============================================================================

//Curve Loop(12) = {77, 26, 27, 78, 53, 54, -67, -66, -65, -58, -57, 72, 73, 32, 75, 76};
//+
//Plane Surface(12) = {5, 9, 12};
//+
//Physical Curve("reflecting", 79) = {26, 27, 28, 29, 30, 31, 32};
//+
Physical Curve("void", 80) = {75, 76, 77, 10077,10076,10075};
//+
