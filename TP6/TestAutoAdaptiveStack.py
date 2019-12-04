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
                    for queue_size in range(5, 10):
                        stack = AutoAdaptiveStack(max_trials, size_increment, queue_size, max_size)
                        
                        self.assertEqual(stack.max_trials, max_trials)
                        self.assertEqual(stack.size_increment, size_increment)
                        self.assertEqual(stack.max_size, max_size)
                        self.assertEqual(stack.waitingQueue.max_size, queue_size)

    def testPushPop(self):
        for size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):
                    
                    queue_size = size_increment

                    stack = AutoAdaptiveStack(max_trials, size_increment, queue_size, size)
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

                    for i in range(max_trials-1):
                        stack.push("queue"+str(i))
                        self.assertEqual(stack.check(), "last")
                        self.assertFalse(stack.isEmpty())
                        self.assertTrue(stack.isFull())
                        self.assertEqual(stack.size(), stackSize)

                    stack.push("lastQueue")

                    max = 0

                    if queue_size >= max_trials:
                        stackSize += max_trials
                        self.assertEqual(stack.check(), "lastQueue")
                        self.assertEqual(stack.pop(), "lastQueue")
                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        stackSize -= 1
                        self.assertEqual(stack.size(), stackSize)
                        max = max_trials-1
                    else:
                        stackSize += queue_size
                        self.assertFalse(stack.isEmpty())
                        self.assertTrue(stack.isFull())
                        self.assertEqual(stack.check(), "queue"+str(queue_size-1))
                        self.assertEqual(stack.size(), stackSize)
                        max = queue_size

                    for i in range(max-1, -1, -1):
                        self.assertEqual(stack.check(), "queue"+str(i))
                        self.assertEqual(stack.pop(), "queue"+str(i))

                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        stackSize -= 1
                        self.assertEqual(stack.size(), stackSize)

                    self.assertEqual(stack.check(), "last")
                    self.assertEqual(stack.pop(), "last")
                    self.assertFalse(stack.isEmpty())
                    self.assertFalse(stack.isFull())
                    stackSize -= 1
                    self.assertEqual(stack.size(), stackSize)

                    for i in range(size-1, 0, -1):
                        self.assertFalse(stack.isEmpty())
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.check(), i)
                        self.assertEqual(stack.pop(), i)
                        stackSize -= 1
                        self.assertEqual(stack.size(), stackSize)

                    self.assertRaises(ValueError, stack.check)
                    self.assertRaises(ValueError, stack.pop)
                    self.assertEqual(stack.size(), 0)
                    self.assertTrue(stack.isEmpty())
                    self.assertFalse(stack.isFull())

#pour tester AutoAdaptiveStack uniquement
if __name__ == '__main__':
    unittest.main()