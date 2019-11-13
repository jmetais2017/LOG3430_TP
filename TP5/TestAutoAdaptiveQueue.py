import unittest
import unittest.mock
import os

from app import AutoAdaptiveQueue

class TestAutoAdaptiveQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        for max_size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):
                    queue = AutoAdaptiveQueue(max_trials, size_increment, max_size)
                    
                    self.assertEqual(queue.max_trials, max_trials)
                    self.assertEqual(queue.size_increment, size_increment)
                    self.assertEqual(queue.max_size, max_size)

    def testEnqueueDequeue(self):
        for size in range(5,10):
            for max_trials in range(5, 10):
                for size_increment in range(5, 10):
                    queue = AutoAdaptiveQueue(max_trials, size_increment, size)
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

                    for n in range(3):
                        for i in range(max_trials-1):
                            queue.enqueue("fail")
                            self.assertEqual(queue.check(), 1)
                            self.assertFalse(queue.isEmpty())
                            self.assertTrue(queue.isFull())
                            self.assertEqual(queue.size(), queueSize)

                        queue.enqueue("fail")
                        self.assertEqual(queue.check(), 1)
                        self.assertFalse(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        self.assertEqual(queue.size(), queueSize)

                        for i in range(1, size_increment):
                            queue.enqueue(i)
                            queueSize += 1

                            self.assertEqual(queue.check(), 1)
                            self.assertFalse(queue.isEmpty())
                            self.assertFalse(queue.isFull())
                            self.assertEqual(queue.size(), queueSize)

                        queue.enqueue("last")
                        queueSize += 1

                        self.assertEqual(queue.check(), 1)
                        self.assertFalse(queue.isEmpty())
                        self.assertTrue(queue.isFull())
                        self.assertEqual(queue.size(), queueSize)

                    for i in range(1, size):
                        self.assertEqual(queue.dequeue(),i)
                        self.assertFalse(queue.isEmpty())
                        self.assertFalse(queue.isFull())
                        queueSize -= 1
                        self.assertEqual(queue.size(), queueSize)

                    self.assertEqual(queue.dequeue(), "last")
                    queueSize -= 1

                    for n in range(3):
                        for i in range(1, size_increment):
                            self.assertEqual(queue.dequeue(),i)
                            self.assertFalse(queue.isEmpty())
                            self.assertFalse(queue.isFull())
                            queueSize -= 1
                            self.assertEqual(queue.size(), queueSize)
                        
                        self.assertEqual(queue.dequeue(), "last")
                        queueSize -= 1

                    self.assertTrue(queue.isEmpty())
                    self.assertFalse(queue.isFull())
                    self.assertEqual(queue.size(), 0)

#pour tester AutoAdaptiveQueue uniquement
if __name__ == '__main__':
    unittest.main()