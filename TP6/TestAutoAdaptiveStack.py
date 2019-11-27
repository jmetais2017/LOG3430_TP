import unittest
import unittest.mock
import os
import io
import sys

from app import AutoAdaptiveStack

class TestAutoAdaptiveStack(unittest.TestCase):

    def setUp(self):
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput  

    def tearDown(self):
        sys.stdout = sys.__stdout__  

    def testInit(self):
        for max_size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):
                    stack = AutoAdaptiveStack(max_trials, size_increment, max_size)
                    
                    self.assertEqual(stack.max_trials, max_trials)
                    self.assertEqual(stack.size_increment, size_increment)
                    self.assertEqual(stack.max_size, max_size)


    def testPushPop(self):
        for size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):
                    stack = AutoAdaptiveStack(max_trials, size_increment, size)
                    stackSize = 0
                    
                    for i in range(1, size):
                        stack.push(i)
                        
                        self.assertEqual(stack.check(), i)
                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        stackSize += 1
                        self.assertEqual(stack.size(), stackSize)

                    stack.push("last")
                    stackSize += 1

                    self.assertEqual(stack.check(), "last")
                    self.assertFalse(stack.isEmpty())
                    self.assertTrue(stack.isFull())
                    self.assertEqual(stack.size(), size)

                    for n in range(3):
                        for i in range(max_trials-1):
                            stack.push("fail")
                            self.assertEqual(stack.check(), "last")
                            self.assertFalse(stack.isEmpty())
                            self.assertTrue(stack.isFull())
                            self.assertEqual(stack.size(), stackSize)

                        stack.push("fail")
                        self.assertEqual(stack.check(), "last")
                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.size(), stackSize)

                        for i in range(1, size_increment):
                            stack.push(i)
                            stackSize += 1

                            self.assertEqual(stack.check(), i)
                            self.assertFalse(stack.isEmpty())
                            self.assertFalse(stack.isFull())
                            self.assertEqual(stack.size(), stackSize)

                        stack.push("last")
                        stackSize += 1

                        self.assertEqual(stack.check(), "last")
                        self.assertFalse(stack.isEmpty())
                        self.assertTrue(stack.isFull())
                        self.assertEqual(stack.size(), stackSize)

                    for n in range(3):

                        self.assertEqual(stack.pop(), "last")
                        stackSize -= 1

                        for i in range(size_increment-1, 0, -1):
                            self.assertEqual(stack.pop(),i)
                            self.assertFalse(stack.isEmpty())
                            self.assertFalse(stack.isFull())
                            stackSize -= 1
                            self.assertEqual(stack.size(), stackSize)

                    self.assertEqual(stack.pop(), "last")
                    stackSize -= 1

                    for i in range(size-1, 1, -1):
                        self.assertEqual(stack.pop(),i)
                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        stackSize -= 1
                        self.assertEqual(stack.size(), stackSize)

                    self.assertEqual(stack.pop(),1)

                    self.assertTrue(stack.isEmpty())
                    self.assertFalse(stack.isFull())
                    self.assertEqual(stack.size(), 0)

#pour tester AutoAdaptiveStack uniquement
if __name__ == '__main__':
    unittest.main()