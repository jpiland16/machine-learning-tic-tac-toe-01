import os, pickle
from Interface import confirm

def get_pickle(ask_confirm: bool=True, use_version: int=-1) -> 'list[int]':
    if not ask_confirm or confirm("begin where the last AI left off?"):
        if use_version == -2:
            return None
        try:
            if use_version == -1:
                use_version = get_latest_ai_version()
            pickle_in = open(os.path.join('store', f'v{use_version}', 
                'data.pickle'), 'rb')
            state_values = pickle.load(pickle_in)
            if ask_confirm:
                print("loaded pickle")
            return state_values
        except:
            print("there was an error loading the pickle")
            return None

def get_latest_ai_version() -> int:
    latest_version = -1
    while (check_ai_version_exists(latest_version + 1)):
        latest_version += 1
    return latest_version

def check_ai_version_exists(v: int) -> bool:
    if not os.path.exists("store"):
        return False
    if not os.path.exists(os.path.join(os.getcwd(), "store", "v" + str(v))):
        return False
    return True


def save_pickle(state_values: 'list[int]', data: str=""):
    version = get_latest_ai_version() + 1

    if not os.path.exists("store"):
        os.mkdir("store")

    if confirm("save the results in a pickle?"):
        os.mkdir(os.path.join("store", f"v{version}"))
        with open(os.path.join("store", f"v{version}", 'data.pickle'),'wb'
            ) as file:
                pickle.dump(state_values, file)
        with open(os.path.join("store", f"v{version}", 'notes.txt'),'w'
            ) as file:
                file.write(data)
