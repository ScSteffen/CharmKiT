import subprocess
import numpy as np
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process some flags for HPC and mesh operations."
    )
    # Add arguments
    parser.add_argument(
        "--no-hpc", action="store_true", help="Flag when using HPC cluster"
    )
    parser.add_argument(
        "--load-from-npz", action="store_true", help="Flag to load from NPZ file"
    )
    parser.add_argument(
        "--no-singularity",
        action="store_true",
        help="Flag to use Singularity Container for KiT-RT",
    )

    args = parser.parse_args()
    return args


def replace_next_line(input_file, custom_line, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "### command below":
            lines[i + 1] = custom_line + "\n"
            break

    with open(output_file, "w") as f:
        f.writelines(lines)


def get_user_job_count(user):
    """
    Get the number of jobs in the SLURM queue for the specified user.
    """
    try:
        # Run the 'squeue' command and filter for the current user
        result = subprocess.run(
            ["squeue", "-u", user],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Get the number of lines in the output, excluding the header line
        job_count = len(result.stdout.strip().split("\n")) - 1
        return job_count
    except Exception as e:
        print(f"Error checking job queue: {e}")
        return 0


def load_hohlraum_samples_from_npz(npz_file):
    samples = np.load(npz_file)["samples"]
    samples[0, :] = 0.4 + (0.2 - samples[0, :])  # tl
    samples[1, :] = -0.4 - (0.2 - samples[1, :])  # bl
    samples[2, :] = 0.4 + (0.2 - samples[2, :])  # tr
    samples[3, :] = -0.4 - (0.2 - samples[3, :])  # br
    samples[4, :] = -0.6 + (samples[4, :] - 0.05)  # wl
    samples[5, :] = +0.6 - (samples[5, :] - 0.05)  # wr

    cl = np.copy(samples[6, :].reshape(1, -1))
    n_quad = np.copy(samples[7, :].reshape(1, -1))
    samples[6, :] = np.zeros(shape=samples[0, :].shape)  # x deviation from center
    samples[7, :] = np.zeros(shape=samples[0, :].shape)  # y deviation from center

    samples_full = np.concatenate((samples, cl, n_quad), axis=0)
    design_param_names = [
        "pos_red_left_top",
        "pos_red_left_bottom",
        "pos_red_right_top",
        "pos_red_right_bottom",
        "pos_red_left_horizontal",
        "pos_red_right_horizontal",
        "pos_green_x",
        "pos_green_y",
        "grid_cl",
        "grid_quad_order",
    ]
    return samples_full, np.array(design_param_names)


def load_hohlraum_samples_from_csv(csv_file="input_samples.csv"):
    import pandas as pd

    df = pd.read_csv(csv_file, header=None)

    # Ensure the CSV has the expected shape
    # assert df.shape == (
    #    128,
    #    6,
    # ), f"CSV file must have shape (128, 6), but got {df.shape}"

    # Transpose to shape (6, 128)
    data = df.to_numpy().T  # shape (6, 128)

    rows = data.shape[1]
    # Create an 8 x 128 array initialized to zero
    result = np.zeros((10, rows))

    # Fill in the first 6 rows with the CSV data
    result[:6, :] = data
    result[8, :] = 0.007 * np.ones((1, rows))
    result[9, :] = 14 * np.ones((1, rows))

    design_param_names = [
        "pos_red_left_top",
        "pos_red_left_bottom",
        "pos_red_right_top",
        "pos_red_right_bottom",
        "pos_red_left_horizontal",
        "pos_red_right_horizontal",
        "pos_green_x",
        "pos_green_y",
        "grid_cl",
        "grid_quad_order",
    ]

    return result, np.array(design_param_names)


def load_quarter_hohlraum_samples_from_npz(npz_file):
    samples = np.load(npz_file)["samples"]
    samples[2, :] = 0.4 + (0.2 - samples[2, :])  # tr
    samples[5, :] = +0.6 - (samples[5, :] - 0.05)  # wr

    cl = np.copy(samples[6, :].reshape(1, -1))
    n_quad = np.copy(samples[7, :].reshape(1, -1))
    samples[6, :] = np.zeros(shape=samples[0, :].shape)  # x deviation from center
    samples[7, :] = np.zeros(shape=samples[0, :].shape)  # y deviation from center

    samples_full = np.concatenate((samples, cl, n_quad), axis=0)
    design_param_names = [
        "pos_red_right_top",
        "pos_red_right_horizontal",
        "grid_cl",
        "grid_quad_order",
    ]
    return samples_full, np.array(design_param_names)


def create_hohlraum_samples_from_param_range(
    parameter_range_n_cell,
    parameter_range_quad_order,
    parameter_range_green_center_x,
    parameter_range_green_center_y,
    parameter_range_red_right_top,
    parameter_range_red_right_bottom,
    parameter_range_red_left_top,
    parameter_range_red_left_bottom,
    parameter_range_horizontal_left,
    parameter_range_horizontal_right,
):
    design_params = []

    for right_red_top in parameter_range_red_right_top:
        for right_red_bottom in parameter_range_red_right_bottom:
            for left_red_top in parameter_range_red_left_top:
                for left_red_bottom in parameter_range_red_left_bottom:
                    for horizontal_left_red in parameter_range_horizontal_left:
                        for horizontal_right_red in parameter_range_horizontal_right:
                            for x_green in parameter_range_green_center_x:
                                for y_green in parameter_range_green_center_y:
                                    for n_cell in parameter_range_n_cell:
                                        for n_quad in parameter_range_quad_order:
                                            design_params.append(
                                                [
                                                    left_red_top,
                                                    left_red_bottom,
                                                    right_red_top,
                                                    right_red_bottom,
                                                    horizontal_left_red,
                                                    horizontal_right_red,
                                                    x_green,
                                                    y_green,
                                                    n_cell,
                                                    n_quad,
                                                ]
                                            )
    design_param_names = [
        "pos_red_left_top",
        "pos_red_left_bottom",
        "pos_red_right_top",
        "pos_red_right_bottom",
        "pos_red_left_horizontal",
        "pos_red_right_horizontal",
        "pos_green_x",
        "pos_green_y",
        "grid_cl",
        "grid_quad_order",
    ]
    return np.array(design_params).T, np.array(design_param_names)


def create_quarter_hohlraum_samples_from_param_range(
    parameter_range_n_cell,
    parameter_range_quad_order,
    parameter_range_red_right_top,
    parameter_range_horizontal_right,
):
    design_params = []

    for right_red_top in parameter_range_red_right_top:
        for horizontal_right_red in parameter_range_horizontal_right:
            for n_cell in parameter_range_n_cell:
                for n_quad in parameter_range_quad_order:
                    design_params.append(
                        [
                            right_red_top,
                            horizontal_right_red,
                            n_cell,
                            n_quad,
                        ]
                    )
    design_param_names = [
        "pos_red_right_top",
        "pos_red_right_bottom",
        "pos_red_right_horizontal",
        "grid_cl",
        "grid_quad_order",
    ]
    return np.array(design_params), np.array(design_param_names)


def load_lattice_samples_from_npz(npz_file):
    print("TODO:load_lattice_samples_from_npz ")
    exit(1)
    return 0


def create_lattice_samples_from_param_range(
    parameter_range_n_cell,
    parameter_range_quad_order,
    parameter_range_abs_blue,
    parameter_range_scatter_white,
):
    design_params = []

    for abs_blue in parameter_range_abs_blue:
        for scatter_white in parameter_range_scatter_white:
            for n_quad in parameter_range_quad_order:
                for n_cell in parameter_range_n_cell:
                    design_params.append(
                        [
                            abs_blue,
                            scatter_white,
                            n_cell,
                            n_quad,
                        ]
                    )

    design_param_names = [
        "absorption_blue",
        "scattering_white",
        "grid_cl",
        "grid_quad_order",
    ]
    return np.array(design_params), np.array(design_param_names)


def delete_slurm_scripts(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    print("Delte all sh files in ", folder_path)
    # Iterate over the files and delete .sh files
    for file in files:
        if file.endswith(".sh"):
            file_path = os.path.join(folder_path, file)

            os.remove(file_path)
