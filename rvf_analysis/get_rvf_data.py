"""
This file contains the necessary functions to collect data from rover vector frame files.
"""
import xml.etree.ElementTree as ET
import pandas as pd

from logs.log_config import get_logger
from lib.rvf_data_fields import REFERENCE_FRAME, OFFSET, ORIENTATION, DERIVATION, SOLUTION_FIELDS, \
    SITE_RVF, RVF_SHEET
from lib.common import RESULTS_EXCEL, get_reference_frame_data, get_offset_data, get_orientation_data, \
    get_derivation_data


class CollectRVFData:
    """
    Collects RVF data from master.rvf files
    """

    def __init__(self, index_value):
        """
        Constructor for CollectRVFData
        :param index_value: index value of the rvf file
        """
        self.logger = get_logger()
        self.index_value = index_value
        self.xml_file = SITE_RVF.format(self.index_value)
        self.xml_data = open(self.xml_file).read()
        self.root = ET.XML(self.xml_data)
        self.rover_frame = None

    def get_results(self, results):
        """
        Converts resultant dataframe to xlsx sheet
        :param results: ExcelWriter object
        :return: None
        """
        rvf_result_sheet = RVF_SHEET.format(self.index_value)
        self.logger.info("Generating xlsx result for {}".format(rvf_result_sheet))
        self.rover_frame.to_excel(results, rvf_result_sheet)

    def collect_rvf_data(self):
        """
        Entry point to collect data from master.rvf file
        :return: None
        """
        self.logger.info("Collecting RVF data")
        rover_frame_fields = [value for i, value in enumerate(self.root) if value.tag == 'solution']
        rover_frame_data = []
        for solution in rover_frame_fields:
            solution_data = {}
            for field in SOLUTION_FIELDS:
                solution_data[field] = solution.attrib[field]
            params = [param for param in solution]
            for param in params:
                if param.tag == 'reference_frame':
                    solution_data = get_reference_frame_data(param, solution_data, REFERENCE_FRAME)
                if param.tag == 'offset':
                    solution_data = get_offset_data(param, solution_data, OFFSET)
                if param.tag == 'orientation':
                    solution_data = get_orientation_data(param, solution_data, ORIENTATION)
                if param.tag == 'derivation':
                    solution_data = get_derivation_data(param, solution_data, DERIVATION)
            rover_frame_data.append(solution_data)
        self.rover_frame = pd.DataFrame(rover_frame_data)


if __name__ == "--main__":
    C = CollectRVFData('000')
    C.collect_rvf_data()
    results = pd.ExcelWriter(RESULTS_EXCEL)
    C.get_results(results)
    results.save()
