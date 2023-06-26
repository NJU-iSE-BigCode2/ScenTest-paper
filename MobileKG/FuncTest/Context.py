from MobileKG.FuncTest.TestNode import TestNode


class Context:

    def __init__(self):
        dummy_head = TestNode('', '', '', '', -1, -1, -1, -1, -1, 'M', '')
        self.cur_opera_node = dummy_head
        self.root = dummy_head
        self.candidate_terminated = False
        self.last_cnt_id = 0
        self.test_node_list = []

    def add_test_node(self, test_node_list):
        self.cur_opera_node.add_next_nodes(test_node_list)
        for node in test_node_list:
            node.set_pre_node(self.cur_opera_node)
        self.cur_opera_node.next_nodes[0].set_operated()
        self.cur_opera_node = self.cur_opera_node.next_nodes[0]
        self.candidate_terminated = self.cur_opera_node.candidate_terminated
        self.last_cnt_id = self.cur_opera_node.cnt_id
        self.test_node_list.append(self.cur_opera_node)

    def same_before(self, test_node):
        for node in self.test_node_list:
            if test_node.equals(node):
                return True
        return False

    def filter_test_node(self, test_node_list):
        res = []
        for node in test_node_list:
            if not self.same_before(node):
                res.append(node)
        return res

    def set_cur_node_operated(self):
        self.cur_opera_node.already_opera = True

    def find_traversal_node(self):
        cur_node = self.cur_opera_node.pre_node
        while cur_node is not None:
            print("cur_node_id:{}".format(cur_node.id))
            if len(cur_node.next_nodes) > 1:
                for node in cur_node.next_nodes:
                    if not node.already_opera:
                        if self.same_before(node):
                            node.set_operated()
                            continue
                        new_opera_node = node
                        test_sequence = []
                        while node.pre_node is not None:
                            test_sequence.append(node)
                            node = node.pre_node
                        test_sequence = test_sequence[::-1]
                        self.cur_opera_node = new_opera_node
                        self.set_cur_node_operated()
                        self.candidate_terminated = self.cur_opera_node.candidate_terminated
                        self.last_cnt_id = self.cur_opera_node.cnt_id
                        return test_sequence
            cur_node = cur_node.pre_node
        return None

    def print(self):
        stack = self.root.next_nodes[::-1]
        stack = [(0, item) for item in stack]
        while len(stack) > 0:
            last_node = stack.pop()
            cur_indentation = last_node[0]
            cur_node = last_node[1]
            space = ""
            for i in range(0, cur_indentation):
                space += "— "
            print(space + cur_node.print())
            next_nodes = cur_node.next_nodes[::-1]
            next_nodes = [(cur_indentation+1, item) for item in next_nodes]
            stack += next_nodes
