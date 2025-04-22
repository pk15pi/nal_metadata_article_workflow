from pid_minter import pid_minter
import pickle

# Path to pkl file
PKL_FILE_PATH = "example_data/pid_minter_example.pkl"

def read_pkl_file():
    citation_object = []
    with open(PKL_FILE_PATH, 'rb') as f:
        citation_object = pickle.load(f)
    return citation_object


def update_pkl_file(citation_object):
    with open(PKL_FILE_PATH, 'wb') as file:
        pickle.dump(citation_object, file)


def mint_pid():
    citation_object = read_pkl_file()
    
    # calling the existing function
    result = pid_minter.pid_minter(citation_object)
    print("message : ", result[1])
    print("PID number is :", result[2])
    update_pkl_file(result[1])
    print("process executed successfully")


mint_pid()
