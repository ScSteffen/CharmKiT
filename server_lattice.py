import umbridge
import time
import os

from src.config_utils import (
    generate_log_filename,
    read_config_file,
    update_parameter,
    write_config_file,
    remove_files,
    update_lattice_mesh_file,
)
from src.scraping_utils import read_csv_file
from src.simulation_utils import run_cpp_simulation_containerized
from src.general_utils import replace_next_line


class KiTRTModelLattice(umbridge.Model):

    def __init__(self):
        super().__init__("forward")

    def get_input_sizes(self, config):
        return [4]

    def get_output_sizes(self, config):
        return [7]

    def __call__(self, parameters, config):

        n_cells = parameters[0][0]
        quad_order = parameters[0][1]

        scatter_white_value = parameters[0][2]
        absorption_blue_value = parameters[0][3]

        subfolder = "benchmarks/lattice/"
        base_config_file = subfolder + "lattice.cfg"

        # Step 1: Read the base config file
        kitrt_parameters = read_config_file(base_config_file)
        lattice_file_new = update_lattice_mesh_file(n_cells, subfolder + "mesh/")

        # Step 2: Update kitrt_parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
        kitrt_parameters = update_parameter(
            kitrt_parameters,
            key="LATTICE_DSGN_ABSORPTION_BLUE",
            new_value=absorption_blue_value,
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters,
            key="LATTICE_DSGN_SCATTER_WHITE",
            new_value=scatter_white_value,
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="QUAD_ORDER", new_value=quad_order
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="MESH_FILE", new_value="mesh/" + lattice_file_new
        )

        # Step 3: Update LOG_FILE to a unique identifier linked to LATTICE_DSGN_ABSORPTION_BLUE
        log_file_cur = f"lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cells}_q{quad_order}"
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
        generated_cfg_file = (
            subfolder
            + f"lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cells}_q{quad_order}.cfg"
        )
        write_config_file(
            parameters=kitrt_parameters, output_file_path=generated_cfg_file
        )

        # Step 5: Run the C++ simulation
        # command = "../../build/KiT-RT " + f'lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cells}_q{quad_order}.cfg'
        # slurm_file = "slurm_" + f'lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cells}_q{quad_order}.sh'
        # replace_next_line("slurm_scripts/slurm_script.txt", command, slurm_file)
        run_cpp_simulation_containerized(generated_cfg_file)

        # Step 6: Read the log file
        log_filename = generate_log_filename(kitrt_parameters)
        if log_filename:
            #    # Step 7: Read and convert the data from the CSV log file to a DataFrame
            log_data = read_csv_file(subfolder + log_filename + ".csv")
            log_data["LATTICE_DSGN_ABSORPTION_BLUE"] = absorption_blue_value
            log_data["LATTICE_DSGN_SCATTER_WHITE"] = scatter_white_value
            quantities_of_interest = [
                float(log_data["Cur_outflow"]),
                float(log_data["Total_outflow"]),
                float(log_data["Max_outflow"]),
                float(log_data["Cur_absorption"]),
                float(log_data["Total_absorption"]),
                float(log_data["Max_absorption"]),
                float(log_data["Wall_time_[s]"]),
            ]

        return [quantities_of_interest]  # [[0]]

    def supports_evaluate(self):
        return True

    def gradient(self, out_wrt, in_wrt, kitrt_parameters, sens, config):
        return 0

    def supports_gradient(self):
        return True


kitrtmodel = KiTRTModelLattice()

umbridge.serve_models([kitrtmodel], 4242)
