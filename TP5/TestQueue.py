import unittest
import unittest.mock
import os

from app import Queue

class TestQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        for size in range(5,10):
            queue = Queue(size)
            self.assertEqual(queue.max_size, size)
            self.assertFalse(queue.isFull())

    def testEnqueueDequeue(self):

        for size in range(5,10):
            queue = Queue(size)

            for i in range(1, size):
                queue.enqueue(i)
                
                self.assertEqual(queue.check(), 1)
                self.assertFalse(queue.isEmpty())
                self.assertFalse(queue.isFull())
                self.assertEqual(queue.size(), i)

            queue.enqueue("last")

            self.assertEqual(queue.check(), 1)
            self.assertFalse(queue.isEmpty())
            self.assertTrue(queue.isFull())
            self.assertEqual(queue.size(), size)

            for i in range(10):
                self.assertRaises(ValueError, queue.enqueue, "fail")

            self.assertEqual(queue.check(), 1)
            self.assertFalse(queue.isEmpty())
            self.assertTrue(queue.isFull())
            self.assertEqual(queue.size(), size)

            queueSize = queue.size()

            for i in range(1, size):
                self.assertEqual(queue.dequeue(),i)
                self.assertFalse(queue.isEmpty())
                self.assertFalse(queue.isFull())
                queueSize -= 1
                self.assertEqual(queue.size(), queueSize)

            self.assertEqual(queue.dequeue(), "last")

            self.assertTrue(queue.isEmpty())
            self.assertFalse(queue.isFull())
            self.assertEqual(queue.size(), 0)


#pour tester Queue uniquement
if __name__ == '__main__':
    unittest.main()