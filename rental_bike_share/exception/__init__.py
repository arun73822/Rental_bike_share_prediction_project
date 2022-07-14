import sys

class Rental_bike_share_Exception(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message=Rental_bike_share_Exception.get_detail_error_message(error_message=error_message,
                                                                                error_details=error_details)

    @staticmethod
    def get_detail_error_message(error_message:Exception,error_details:sys)->str:

        _,_ ,exec_tb=error_details.exc_info()
        try_block_no=exec_tb.tb_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename
        exception_block_file_no=exec_tb.tb_frame.f_lineno

        error_message=f"""The file name is {[ file_name ]} and
                          Try block line number is {try_block_no} and 
                          exception line number is {exception_block_file_no}"""

        return error_message
    
    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return Rental_bike_share_Exception.__name__.str()
