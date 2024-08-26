import numpy as np
from src.models.hohlraum import get_qois_col_names, model


from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_hohlraum_samples_from_param_range,
    load_hohlraum_samples_from_npz,
    delete_slurm_scripts,
)
from src.general_utils import parse_args


def main():
    args = parse_args()
    print(f"HPC mode = { not args.no_hpc}")
    print(f"Load from npz = {args.load_from_npz}")
    print(f"HPC with singularity = { not args.no_singularity_hpc}")

    hpc_operation = not args.no_hpc  # Flag when using HPC cluster
    load_from_npz = args.load_from_npz
    singularity_hpc = not args.no_singularity_hpc

    # Define parameter ranges
    parameter_range_n_cell =  [
        0.01,
        0.0075,
        0.005,
        0.0025,
        0.001,
        0.00075,
        0.0005,
        0.00025
    ]  # characteristic length of the cells
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)
    parameter_range_quad_order = [4, 8, 12, 16, 20, 24, 28,32,40,44,48,52,56,60,64,68,72,76,80]  # , 20, 30, 40, 50]
    parameter_range_green_center_x = [0.0]  # [0.0, 0.01, -0.01]
    parameter_range_green_center_y = [0.0]  # [0.0, 0.01, -0.01]
    parameter_range_red_right_top = [0.4]  # [0.4, 0.45, 0.35]
    parameter_range_red_right_bottom = [-0.4]  # [-0.4, -0.45, -0.35]
    parameter_range_red_left_top = [0.4]  # [0.4, 0.45, 0.35]
    parameter_range_red_left_bottom = [-0.4]  # [-0.4, -0.45, -0.35]
    parameter_range_horizontal_left = [-0.6]  # [-0.6, -0.61, -0.59]
    parameter_range_horizontal_right = [0.6]  # [0.6, 0.61, 0.59]

    if load_from_npz:
        design_params, design_param_names = load_hohlraum_samples_from_npz(
            "sampling/pilot-study-samples-hohlraum-05-29-24.npz"
        )
    else:
        design_params, design_param_names = create_hohlraum_samples_from_param_range(
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
        )

    if hpc_operation:
        print("==== Execute HPC version ====")
        directory = "./benchmarks/hohlraum/slurm_scripts/"
        user = read_username_from_config("./slurm_config.txt")

        delete_slurm_scripts(directory)  # delete existing slurm files for hohlraum
        call_models(
            design_params, hpc_operation_count=1, singularity_hpc=singularity_hpc
        )
        # wait_for_slurm_jobs(user=user, sleep_interval=10)

        if user:
            print("Executing slurm scripts with user " + user)
            execute_slurm_scripts(directory, user)
            wait_for_slurm_jobs(user=user, sleep_interval=10)
        else:
            print("Username could not be read from slurm config file.")
        qois = call_models(design_params, hpc_operation_count=2)
    else:
        qois = call_models(
            design_params, hpc_operation_count=0, singularity_hpc=singularity_hpc
        )

    print("design parameter matrix")
    print(design_param_names)
    print(design_params)
    print("quantities of interest:")
    print(get_qois_col_names())
    print(qois)
    np.savez(
        "benchmarks/hohlraum/sn_study_hohlraum.npz",
        qois=qois,
        design_params=design_params,
        qoi_column_names=get_qois_col_names(),
        design_param_column_names=design_param_names,
    )

    print("======== Finished ===========")
    return 0


def call_models(design_params, hpc_operation_count, singularity_hpc=True):
    qois = []
    for column in design_params.T:
        input = column.tolist()
        input.append(hpc_operation_count)
        input.append(singularity_hpc)
        res = model([input])
        qois.append(res[0])

    return np.array(qois)


if __name__ == "__main__":
    main()
