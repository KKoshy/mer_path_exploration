"""
This file comprises of the necessary functions to collect data from site vector frame file.
"""

import os
import shutil
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.common import (
    DATA_ZIP,
    RESULTS_EXCEL,
    RESULTS_PLOT,
    get_derivation_data,
    get_offset_data,
    get_orientation_data,
    get_reference_frame_data,
)
from lib.svf_data_fields import (
    DATA_DIR,
    DERIVATION,
    MASTER_SVF,
    NUMERIC_FIELDS,
    OFFSET,
    ORIENTATION,
    REFERENCE_FRAME,
    SOLUTION_FIELDS,
    SVF_SHEET,
)
from logs.log_config import get_logger
from rvf_analysis.get_rvf_data import CollectRVFData


class CollectSVFData:
    """
    Collects SVF data master.svf file
    """

    def __init__(self):
        """
        Constructor for CollectSVFData
        """
        self.logger = get_logger()
        self.unzip_data_files()
        self.xml_data = open(MASTER_SVF).read()
        self.root = ET.XML(self.xml_data)
        self.site_frame = None

    def get_graphical_result(self):
        """
        Creates 3-dimensional plot based on svf x, y, z co-ordinates
        :return: None
        """
        self.logger.info(
            "Generating path traced by MER2 as 3-dimensional interactive plot"
        )
        x, y, z = self.site_frame["x"], self.site_frame["y"], self.site_frame["z"]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot3D(x, y, z, "green", label="svf_data_path")
        ax.set_title("Site Vector Frame Data Analysis (Path traced by MER2)")
        ax.set_xlabel("$X$")
        ax.set_ylabel("$Y$")
        ax.set_zlabel("$Z$")
        ax.legend(loc="upper left")
        plt.savefig(RESULTS_PLOT, dpi=1080)
        self.logger.info("Close the plot to continue execution")
        plt.show()

    def get_results(self, results):
        """
        Converts the results to xlsx sheets
        :param: results: object to insert xlsx sheet
        :return: None
        """
        self.logger.info("Generating SVF results as xlsx file")
        self.site_frame.to_excel(results, SVF_SHEET)

    def collect_rvf_from_svf(self, results):
        """
        Collects rover frame data from site frame data by using reference frame index1
        :param results: object to insert xlsx sheet
        :return: None
        """
        self.logger.info("Collecting RVF data from SVF")
        rvf_data_frames = self.site_frame["ref_frame_index1"].to_list()
        for rvf_data_frame in rvf_data_frames:
            R = CollectRVFData(rvf_data_frame.zfill(3))
            R.collect_rvf_data()
            R.get_results(results)

    def unzip_data_files(self):
        """
        Unzips the data zip file
        :return: None
        """
        self.logger.info("Extracting files from zip file")
        with ZipFile(DATA_ZIP) as zipObj:
            zipObj.extractall()

    def remove_data_dir(self):
        """
        Removes data directory
        :return: None
        """
        self.logger.info("Removing data directory")
        shutil.rmtree(DATA_DIR)

    def collect_svf_data(self):
        """
        Entry point to collect data from master.svf file
        :return: None
        """
        self.logger.info("Collecting SVF data")
        site_frame_fields = [
            value for i, value in enumerate(self.root) if value.tag == "solution"
        ]
        site_frame_data = []
        for solution in site_frame_fields:
            solution_data = {}
            for field in SOLUTION_FIELDS:
                solution_data[field] = solution.attrib[field]
            params = [param for param in solution]
            for param in params:
                if param.tag == "reference_frame":
                    solution_data = get_reference_frame_data(
                        param, solution_data, REFERENCE_FRAME
                    )
                if param.tag == "offset":
                    solution_data = get_offset_data(param, solution_data, OFFSET)
                if param.tag == "orientation":
                    solution_data = get_orientation_data(
                        param, solution_data, ORIENTATION
                    )
                if param.tag == "derivation":
                    solution_data = get_derivation_data(
                        param, solution_data, DERIVATION
                    )
            site_frame_data.append(solution_data)
        self.site_frame = pd.DataFrame(site_frame_data)
        self.site_frame[NUMERIC_FIELDS] = self.site_frame[NUMERIC_FIELDS].apply(
            pd.to_numeric
        )
        self.get_graphical_result()


if __name__ == "__main__":
    C = CollectSVFData()
    results = pd.ExcelWriter(RESULTS_EXCEL)
    C.collect_svf_data()
    C.get_results(results)
    C.collect_rvf_from_svf(results)
    C.remove_data_dir()
    results.close()
