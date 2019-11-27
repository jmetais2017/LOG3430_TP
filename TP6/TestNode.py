import unittest
import unittest.mock
import os
from app import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        for i in range(5):
            node = Node(i)
            self.assertEqual(node.value, i)
            self.assertEqual(str(node), str(i))
            self.assertIsNone(node.next)

    def testNext(self):
        node = Node(-1)

        for i in range(5):
            node.next = Node(i)
            node = node.next
            self.assertEqual(node.value, i)
            self.assertEqual(str(node), str(i))
            self.assertIsNone(node.next)




#pour tester Node uniquement
if __name__ == '__main__':
    unittest.main()