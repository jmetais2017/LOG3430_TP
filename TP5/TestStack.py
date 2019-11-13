import unittest
import unittest.mock
import os

from app import Stack

class TestStack(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        for size in range(5,10):
            stack = Stack(size)
            self.assertEqual(stack.max_size, size)
            self.assertFalse(stack.isFull())

    def testPushPop(self):
        for size in range(5,10):
            stack = Stack(size)

            for i in range(1, size):
                stack.push(i)
                self.assertEqual(stack.size(), i)
                self.assertEqual(stack.check(), i)

                self.assertFalse(stack.isEmpty())
                self.assertFalse(stack.isFull())

            stack.push("last")

            self.assertEqual(stack.size(), size)
            self.assertEqual(stack.check(), "last")
            
            self.assertFalse(stack.isEmpty())
            self.assertTrue(stack.isFull())

            for i in range(10):
                self.assertRaises(ValueError, stack.push, "fail")

            self.assertEqual(stack.size(), size)
            self.assertEqual(stack.check(), "last")
            
            self.assertFalse(stack.isEmpty())
            self.assertTrue(stack.isFull())

            self.assertEqual(stack.pop(), "last")

            for i in range(size-1, 1, -1):
                self.assertEqual(stack.pop(), i)

                self.assertFalse(stack.isEmpty())
                self.assertFalse(stack.isFull())

            self.assertEqual(stack.pop(), 1)
            
            self.assertTrue(stack.isEmpty())
            self.assertFalse(stack.isFull())


#pour tester Stack uniquement
if __name__ == '__main__':
    unittest.main()