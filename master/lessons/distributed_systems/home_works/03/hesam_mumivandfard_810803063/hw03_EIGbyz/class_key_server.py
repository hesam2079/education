class PublicKeyServer:
    def __init__(self, number_of_processes):
        self.list_of_keys = number_of_processes * [None]

    def add_key(self, key, process_number):
        self.list_of_keys[process_number] = key

    def get_key(self, process_number):
        return self.list_of_keys[process_number]