"""
This file contains data and functions which are common for rvf and svf data analysis
"""
import os
from datetime import datetime

RESULTS_EXCEL = os.path.join("reports",
                             "mer_result_analysis_{}.xlsx".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
RESULTS_PLOT = os.path.join("reports",
                            "mer_result_plot_{}.png".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
DATA_ZIP = "data.zip"
LOG_FILE = os.path.join("logs", "mer_path_exploration_{}.log".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

def get_reference_frame_data(param, solution_data, ref_frame):
    """
    Collects data from reference frame tag under each solution element
    :param param:
    :param solution_data:
    :param ref_frame: reference fields for the data
    :return: updated solution_data
    """
    for field in ref_frame:
        solution_data['ref_frame_' + field] = param.attrib[field]
    return solution_data


def get_offset_data(param, solution_data, offset):
    """
    Collects data from offset tag under each solution element
    :param param:
    :param solution_data:
    :param offset: reference fields for offset data
    :return: updated solution_data
    """
    for field in offset:
        solution_data[field] = param.attrib[field]
    return solution_data


def get_orientation_data(param, solution_data, orientation):
    """
    Collects data from orientation tag under each solution element
    :param param:
    :param solution_data:
    :param orientation: reference fields for orientation data
    :return: updated solution_data
    """
    for field in orientation:
        solution_data[field] = param.attrib[field]
    return solution_data


def get_derivation_data(param, solution_data, derivation):
    """
    Collects data from derivation tag under each solution element
    :param param:
    :param solution_data:
    :param derivation: reference fields for derivation data
    :return: updated solution_data
    """
    for field in derivation:
        solution_data['derive_' + field] = param.attrib[field]
    return solution_data
