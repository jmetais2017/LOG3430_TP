import unittest
import unittest.mock
import os

from app import LinkedList, Queue, Stack, Calculator

def contient(liste, valeur):
    
    for elem in liste.list:
        if elem == valeur:
            return True

    return False

class TestCalculator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInvalidUnion(self):
        for obj in [LinkedList(), Stack(5), Queue(5)]:
            for invalid in [1, "fail", -3.4]:
                self.assertRaises(ValueError, Calculator.union, obj, invalid)


    def testUnionTwoLinkedLists(self):

        listes = []

        for n in range(5):
            liste = LinkedList()

            for i in range(10):
                liste.append(i + n*100)

            listes.append(liste)

        for i in range(len(listes)):
            for j in range(i):
                resultat = Calculator.union(listes[i], listes[j])

                self.assertIsInstance(resultat, LinkedList)
                self.assertNotIsInstance(resultat, Stack)
                self.assertNotIsInstance(resultat, Queue)

                self.assertEqual(resultat.size(), listes[i].size() + listes[j].size())

                for k in range(len(listes)):
                    if k==i:
                        for elem in listes[k].list:
                            self.assertTrue(contient(resultat, elem))
                            
                    elif k==j:
                        for elem in listes[k].list:
                            self.assertTrue(contient(resultat, elem))
                    else:
                        for elem in listes[k].list:
                            self.assertFalse(contient(resultat, elem))

    def testUnionStackAndQueue(self):
        stacks = []

        for n in range(5):
            stack = Stack(20)

            for i in range(10):
                stack.push(i+n*100)

            stacks.append(stack)

        queues = []

        for n in range(5):
            queue = Queue(20)

            for i in range(10):
                queue.enqueue(i+n*1000)

            queues.append(queue)

        for stack in stacks:
            for queue in queues:
                resultat = Calculator.union(stack, queue)

                self.assertIsInstance(resultat, LinkedList)
                self.assertNotIsInstance(resultat, Stack)
                self.assertNotIsInstance(resultat, Queue)

                self.assertEqual(resultat.size(), stack.size() + queue.size())


                for elem in stack.list:
                    self.assertTrue(contient(resultat, elem))

                for elem in queue.list:
                    self.assertTrue(contient(resultat, elem))

    def testUnionTwoStacks(self):

        for i in range(5):
            for j in range(5):

                stack1 = Stack(20)

                for k in range(10):
                    stack1.push(k+i*100)

                stack2 = Stack(20)

                for k in range(10):
                    stack2.push(k+j*1000)

                resultat = Calculator.union(stack1, stack2)

                self.assertIsInstance(resultat, Stack)

                self.assertEqual(resultat.max_size, stack1.max_size + stack2.max_size)
                self.assertEqual(resultat.size(), stack1.size() + stack2.size())

                for k in range(9, -1, -1):
                    self.assertEqual(resultat.pop(), k+j*1000)

                for k in range(9, -1, -1):
                    self.assertEqual(resultat.pop(), k+i*100)

    def testUnionTwoQueues(self):

        for i in range(5):
            for j in range(5):

                queue1 = Queue(20)

                for k in range(10):
                    queue1.enqueue(k+i*100)

                queue2 = Queue(20)

                for k in range(10):
                    queue2.enqueue(k+j*1000)

                resultat = Calculator.union(queue1, queue2)

                self.assertIsInstance(resultat, Queue)

                self.assertEqual(resultat.max_size, queue1.max_size + queue2.max_size)
                self.assertEqual(resultat.size(), queue1.size() + queue2.size())

                for k in range(10):
                    self.assertEqual(resultat.dequeue(), k+i*100)

                for k in range(10):
                    self.assertEqual(resultat.dequeue(), k+j*1000)

#pour tester Calculator uniquement
if __name__ == '__main__':
    unittest.main()