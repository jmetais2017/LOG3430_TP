import unittest
import unittest.mock
import os
import io
import sys

from app import AutoAdaptiveQueue

class TestAutoAdaptiveQueue(unittest.TestCase):

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
                        queue = AutoAdaptiveQueue(max_trials, size_increment, queue_size, max_size)
                        
                        self.assertEqual(queue.max_trials, max_trials)
                        self.assertEqual(queue.size_increment, size_increment)
                        self.assertEqual(queue.max_size, max_size)
                        self.assertEqual(queue.waitingQueue.max_size, queue_size)

    def testEnqueueDequeue(self):
        for size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):

                    queue_size = size_increment

                    queue = AutoAdaptiveQueue(max_trials, size_increment, queue_size, size)
                    queueSize = 0
                    
                    for i in range(1, size):
                        queue.enqueue(i)
                        
                        self.assertEqual(queue.check(), 1)
                        self.assertFalse(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        queueSize += 1
                        self.assertEqual(queue.size(), queueSize)

                    queue.enqueue("last")
                    queueSize += 1

                    self.assertEqual(queue.check(), 1)
                    self.assertFalse(queue.isEmpty())
                    self.assertTrue(queue.isFull())
                    self.assertEqual(queue.size(), size)

                    for i in range(max_trials-1):
                        queue.enqueue("queue"+str(i))
                        self.assertEqual(queue.check(), 1)
                        self.assertFalse(queue.isEmpty())
                        self.assertTrue(queue.isFull())
                        self.assertEqual(queue.size(), queueSize)

                    queue.enqueue("lastQueue")

                    for i in range(1, size):
                        self.assertFalse(queue.isEmpty())
                        queueSize = queue.size()
                        self.assertEqual(queue.check(), i)
                        self.assertEqual(queue.dequeue(), i)
                        queueSize -= 1
                        self.assertEqual(queue.size(), queueSize)

                    self.assertEqual(queue.check(), "last")
                    self.assertEqual(queue.dequeue(), "last")
                    self.assertFalse(queue.isEmpty())
                    self.assertFalse(queue.isFull())
                    queueSize -= 1
                    self.assertEqual(queue.size(), queueSize)

                    for i in range(queue.size()-1):
                        self.assertEqual(queue.check(), "queue"+str(i))
                        self.assertEqual(queue.dequeue(), "queue"+str(i))

                        self.assertFalse(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        queueSize -= 1
                        self.assertEqual(queue.size(), queueSize)

                    if queue_size >= max_trials:
                        self.assertEqual(queue.check(), "lastQueue")
                        self.assertEqual(queue.dequeue(), "lastQueue")
                        self.assertTrue(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        queueSize -= 1
                        self.assertEqual(queue.size(), queueSize)
                    else:
                        self.assertEqual(queue.check(), "queue"+str(queue_size-1))
                        self.assertEqual(queue.dequeue(), "queue"+str(queue_size-1))
                        self.assertTrue(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        queueSize -= 1
                        self.assertEqual(queue.size(), queueSize)

                    self.assertRaises(ValueError, queue.check)
                    self.assertRaises(ValueError, queue.dequeue)
                    self.assertEqual(queue.size(), 0)
                    self.assertTrue(queue.isEmpty())
                    self.assertFalse(queue.isFull())

#pour tester AutoAdaptiveQueue uniquement
if __name__ == '__main__':
    unittest.main()