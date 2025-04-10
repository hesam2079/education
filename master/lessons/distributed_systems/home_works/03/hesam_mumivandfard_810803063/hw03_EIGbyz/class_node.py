""" in this class we have two methods and three values
value for value of node 0,1
path is string of x in pseudocode
and leaf flag is flag that if it is true then the node is leaf else node is non leaf

method new_val calculate the new value of node
method get_val return the value of node """

class Node:
    def __init__(self, value, path, leaf_flag=True):
        self.value = value
        self.path = path
        self.leaf_flag = leaf_flag

    def __repr__(self):
        message = "value:"+ str(self.value)+ " path:"+ str(self.path)+ " leaf_flag:"+str(self.leaf_flag)
        return message