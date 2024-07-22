#!/usr/bin/env python3
"""
Simple pagination
"""

import csv
from typing import List
from index_range import index_range  # Ensure index_range is imported correctly

class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude the header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return the appropriate page of the dataset.

        Parameters:
        page (int): The page number to retrieve (1-indexed).
        page_size (int): The number of items per page.

        Returns:
        List[List]: A list of lists representing the rows of the dataset for the requested page.
        """
        # Validate arguments
        assert isinstance(page, int) and page > 0, "Page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "Page size must be a positive integer"

        # Get the start and end index for pagination
        start_index, end_index = index_range(page, page_size)
        
        # Retrieve the dataset
        data = self.dataset()
        
        # Return the page of data
        return data[start_index:end_index]

