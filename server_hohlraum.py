import umbridge
import time
import os

from src.config_utils import (
    generate_log_filename,
    read_config_file,
    update_parameter,
    write_config_file,
    remove_files,
    update_sym_hohlraum_mesh_file,
)
from src.scraping_utils import read_csv_file
from src.simulation_utils import run_cpp_simulation_containerized
from src.general_utils import replace_next_line


class KiTRTModelHohlraum(umbridge.Model):

    def __init__(self):
        super().__init__("forward")

    def get_input_sizes(self, config):
        return [8]

    def get_output_sizes(self, config):
        return [17]

    def __call__(self, parameters, config):

        n_cells = parameters[0][0]
        quad_order = parameters[0][1]
        x_green = parameters[0][2]
        y_green = parameters[0][3]
        right_red_top = parameters[0][4]
        right_red_bottom = parameters[0][5]
        left_red_top = parameters[0][6]
        left_red_bottom = parameters[0][7]

        subfolder = "benchmarks/hohlraum/"
        base_config_file = subfolder + "hohlraum.cfg"

        # Step 1: Read the base config file
        kitrt_parameters = read_config_file(base_config_file)
        hohlraum_file_new = update_sym_hohlraum_mesh_file(n_cells, subfolder + "mesh/")

        # Step 2: Update kitrt_parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="QUAD_ORDER", new_value=quad_order
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="MESH_FILE", new_value="mesh/" + hohlraum_file_new
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_CENTER_X", new_value=x_green
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_CENTER_Y", new_value=y_green
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_RED_RIGHT_TOP", new_value=right_red_top
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_RED_RIGHT_BOTTOM", new_value=right_red_bottom
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_RED_LEFT_TOP", new_value=left_red_top
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="POS_RED_LEFT_BOTTOM", new_value=left_red_bottom
        )

        # Step 3: Update LOG_FILE to a unique identifier linked to LATTICE_DSGN_ABSORPTION_BLUE
        log_file_cur = f"hohlraum_n{n_cells}_q{quad_order}_x{x_green}_y{y_green}_r{right_red_top}_{right_red_bottom}_l{left_red_top}_{left_red_bottom}"
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="LOG_FILE", new_value=log_file_cur
        )
        remove_files(subfolder + kitrt_parameters["LOG_DIR"] + "/" + log_file_cur)
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="OUTPUT_FILE", new_value=log_file_cur
        )
        remove_files(
            subfolder + kitrt_parameters["OUTPUT_DIR"] + "/" + log_file_cur + ".vtk"
        )

        # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
        generated_cfg_file = subfolder + f"hohlraum_n{n_cells}_q{quad_order}.cfg"
        write_config_file(
            parameters=kitrt_parameters, output_file_path=generated_cfg_file
        )

        # Step 5: Run the C++ simulation
        command = "../../build/KiT-RT " + f"hohlraum_n{n_cells}_q{quad_order}.cfg"
        slurm_file = "slurm_" + f"hohlraum_n{n_cells}_q{quad_order}.sh"
        # replace_next_line("slurm_scripts/slurm_script.txt", command, slurm_file)
        run_cpp_simulation_containerized(generated_cfg_file)

        # Step 6: Read the log file
        log_filename = generate_log_filename(kitrt_parameters)
        if log_filename:
            # Step 7: Read and convert the data from the CSV log file to a DataFrame
            log_data = read_csv_file(subfolder + log_filename + ".csv")
            quantities_of_interest = [
                float(log_data["Wall_time_[s]"]),
                float(log_data["Cumulated_absorption_center"]),
                float(log_data["Cumulated_absorption_vertical_wall"]),
                float(log_data["Cumulated_absorption_horizontal_wall"]),
                float(log_data["Var. absorption green"]),
                float(log_data["Probe 0 u_0"]),
                float(log_data["Probe 0 u_1"]),
                float(log_data["Probe 0 u_2"]),
                float(log_data["Probe 1 u_0"]),
                float(log_data["Probe 1 u_1"]),
                float(log_data["Probe 1 u_2"]),
                float(log_data["Probe 2 u_0"]),
                float(log_data["Probe 2 u_1"]),
                float(log_data["Probe 2 u_2"]),
                float(log_data["Probe 3 u_0"]),
                float(log_data["Probe 3 u_1"]),
                float(log_data["Probe 3 u_2"]),
            ]
        # quantities_of_interest = [0]
        return [quantities_of_interest]

    def supports_evaluate(self):
        return True

    def gradient(self, out_wrt, in_wrt, kitrt_parameters, sens, config):
        return 0

    def supports_gradient(self):
        return True


kitrtmodel = KiTRTModelHohlraum()

umbridge.serve_models([kitrtmodel], 4242)
