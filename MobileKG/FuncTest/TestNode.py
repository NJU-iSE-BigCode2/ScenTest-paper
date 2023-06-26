class TestNode:

    def __init__(self, category, text, operation, cnt, cnt_id, x1, y1, x2, y2, terminated, activity,
                 pre_node=None, tag=-1):
        self.widget_category = category
        self.ocr_text = text
        self.widget_operation = operation
        self.cnt = cnt
        self.cnt_id = cnt_id
        self.left = x1
        self.right = x2
        self.top = y1
        self.bottom = y2
        self.already_opera = False
        if terminated == 'M':
            self.candidate_terminated = False
        else:
            self.candidate_terminated = True
        self.next_nodes = []
        self.pre_node = pre_node
        self.id = tag
        self.activity_name = activity

    def add_next_nodes(self, nodes_list):
        self.next_nodes = nodes_list
        for node in nodes_list:
            node.set_pre_node(self)

    def set_pre_node(self, node):
        self.pre_node = node

    def set_operated(self):
        self.already_opera = True

    def equals(self, test_node):
        if self.activity_name == test_node.activity_name and self.ocr_text == test_node.ocr_text and self.widget_operation == test_node.widget_operation and self.left == test_node.left and self.right == test_node.left and self.top == test_node.top and self.bottom == test_node.bottom:
            return True
        else:
            return False

    def print(self):
        text = "node: cur_id:{}, category:{}, test:{}, operation:{}, cnt:{}, cnt_id:{}, x1:{}, y1:{}, x2:{}, y2:{}, pre_node:{}".format(
            self.id, self.widget_category, self.ocr_text, self.widget_operation, self.cnt, self.cnt_id, self.left,
            self.top, self.right, self.bottom, self.pre_node.id)
        return text
