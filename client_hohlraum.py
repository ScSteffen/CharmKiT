import umbridge

url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix
# 10 means that the green hohlraum device is 10 grid cells thick. rest of the domain is meshed a bit coarser but accordingly
parameter_range_n_cell = [5]  # [10, 20, 40]
# GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)
parameter_range_quad_order = [10]  # , 20, 30, 40, 50]
parameter_range_green_center_x = [0.0, 0.01, -0.01]
parameter_range_green_center_y = [0.0, 0.01, -0.01]
parameter_range_red_right_top = [0.4, 0.45, 0.35]
parameter_range_red_right_bottom = [-0.4, -0.45, -0.35]
parameter_range_red_left_top = [0.4, 0.45, 0.35]
parameter_range_red_left_bottom = [-0.4, -0.45, -0.35]

design_params = []
qois = []

# with open("slurm_scripts/slurm_run_all_sym_hohlraum.sh", "w") as file:
for n_cell in parameter_range_n_cell:
    for n_quad in parameter_range_quad_order:
        for x_green in parameter_range_green_center_x:
            for y_green in parameter_range_green_center_y:
                for right_red_top in parameter_range_red_right_top:
                    for right_red_bottom in parameter_range_red_right_bottom:
                        for left_red_top in parameter_range_red_left_top:
                            for left_red_bottom in parameter_range_red_left_bottom:
                                design_params.append(
                                    [
                                        n_cell,
                                        n_quad,
                                        x_green,
                                        y_green,
                                        right_red_top,
                                        right_red_bottom,
                                        left_red_top,
                                        left_red_bottom,
                                    ]
                                )
                                res = model(
                                    [
                                        [
                                            n_cell,
                                            n_quad,
                                            x_green,
                                            y_green,
                                            right_red_top,
                                            right_red_bottom,
                                            left_red_top,
                                            left_red_bottom,
                                        ]
                                    ]
                                )
                                qois.append(res[0])
#            file.write(f'sbatch slurm_scripts/slurm_sym_hohlraum_n{n_cell}_q{n_quad}.sh\n')

# with open("slurm_scripts/run_all_sym_hohlraum.sh", "w") as file:
#     for n_cell in parameter_range_n_cell:
#        for n_quad in parameter_range_quad_order:
#            file.write(f'../../build/KiT-RT sym_hohlraum_n{n_cell}_q{n_quad}.cfg\n')

# run model and print output
print("design parameter matrix")
print(design_params)
print(
    "quantities of interest: [ Wall_time_[s],  Cumulated_absorption_center,Cumulated_absorption_vertical_wall,Cumulated_absorption_horizontal_wall,Var. absorption green,Probe 0 u_0,Probe 0 u_1,Probe 0 u_2,Probe 1 u_0,Probe 1 u_1,Probe 1 u_2, Probe 3 u_0,Probe 3 u_1,Probe 3 u_2,Probe 4 u_0,Probe 4 u_1,Probe 4 u_2]"
)
print(qois)
print("======== Finished ===========")
