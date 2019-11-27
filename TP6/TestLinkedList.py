import unittest
import unittest.mock
import os

from app import LinkedList

class TestLinkedList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        linkedList = LinkedList()

        self.assertTrue(linkedList.isEmpty())
        self.assertEqual(linkedList.size(),0)

        self.assertRaises(ValueError, linkedList.check)
        self.assertRaises(ValueError, linkedList.peek)

    def testAppendPeek(self):
        linkedList = LinkedList()
        linkedList.append("debut")

        for i in range(5):
            linkedList.append(i)
            self.assertEqual(linkedList.check(), "debut")
            self.assertFalse(linkedList.isEmpty())
            self.assertEqual(linkedList.size(), i+2)

        self.assertEqual(linkedList.peek(), "debut")

        listSize = linkedList.size()

        for i in range(4):
            self.assertEqual(linkedList.peek(), i)
            self.assertFalse(linkedList.isEmpty())
            listSize -= 1
            self.assertEqual(linkedList.size(), listSize)

        self.assertEqual(linkedList.peek(), 4)
    
        self.assertTrue(linkedList.isEmpty())
        self.assertEqual(linkedList.size(),0)

        self.assertRaises(ValueError, linkedList.check)
        self.assertRaises(ValueError, linkedList.peek)

    def testPrependPeek(self):
        linkedList = LinkedList()
        linkedList.append("debut")

        for i in range(5):
            linkedList.prepend(i)
            self.assertEqual(linkedList.check(), i)
            self.assertFalse(linkedList.isEmpty())
            self.assertEqual(linkedList.size(), i+2)

        listSize = linkedList.size()

        for i in range(4, -1, -1):
            self.assertEqual(linkedList.peek(), i)
            self.assertFalse(linkedList.isEmpty())
            listSize -= 1
            self.assertEqual(linkedList.size(), listSize)

        self.assertEqual(linkedList.peek(), "debut")
    
        self.assertTrue(linkedList.isEmpty())
        self.assertEqual(linkedList.size(),0)

        self.assertRaises(ValueError, linkedList.check)
        self.assertRaises(ValueError, linkedList.peek)



#pour tester LinkedList uniquement
if __name__ == '__main__':
    unittest.main()