import sys


def error_message_detail(error, error_detail: sys):
    """
    Extracts the error message, including the file name and line number where the error occurred.
    """
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in [{file_name}] line number [{line_number}] error message [{str(error)}]"
    else:
        error_message = str(error)

    return error_message


class CustomException(Exception):
    """
    A custom exception class that captures and formats detailed error information,
    including the script name and line number.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        print(CustomException(e, sys))
