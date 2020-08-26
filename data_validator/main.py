from file_existence import init_file_existence


# Declare config varibles here before running the init_validator script
file_directory = '/Users/ericlingren/Desktop'


def init_validator():
    init_file_existence(file_directory)


init_validator()
