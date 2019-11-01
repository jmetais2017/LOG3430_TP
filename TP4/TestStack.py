import unittest
import unittest.mock
import os
from Stack import Stack

class TestQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #test du chemin empty-pop
    def test_path_empty_pop(self):
        stack = Stack(5, 5, 5)

        #verification de l'etat initial
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertEqual(str(stack),"|")

        #tester le chemin a laide la fonction pop
        self.assertRaises(ValueError, stack.pop)

    #test du chemin empty-push-normal-pop-empty
    def test_path_empty_push_normal_pop_empty(self):
        stack = Stack(5,5,5)

        #verification de l'etat initial
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertEqual(str(stack),"|")

        #tester la transition
        stack.push("first")

        #verification de l'etat normal
        self.assertFalse(stack.isEmpty())
        self.assertEqual(stack.size(), 1)
        self.assertFalse(stack.isFull())
        self.assertEqual(stack.peek(), "first")
        self.assertEqual(str(stack),"|first|")

        #tester la transition
        self.assertEqual(stack.pop(),"first")

        #verification de l'etat empty
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")

    #tester le chemin empty-(push-normal)*-(pop-normal)*-pop-empty
    def test_path_multiple_push(self):

        #tester divers choix de tailles
        for size in range(3, 10):
            stack = Stack(20, 20, 20)

            #verification de l'etat initial
            self.assertTrue(stack.isEmpty())
            self.assertEqual(stack.size(), 0)
            self.assertFalse(stack.isFull())
            self.assertRaises(ValueError, stack.peek)
            self.assertEqual(str(stack),"|")

            s = "|"

            #tester le push size fois
            for k in range(1, size):

                #tester la transition
                stack.push(k)
                s = "|"+str(k)+s

                #tester l'etat normal
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)
                self.assertEqual(str(stack),s)

            #tester le pop size fois
            for k in range(size-1, 0, -1):

                #tester l'etat normal
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)

                #tester la transition
                self.assertEqual(stack.pop(), k)

        #tester l'etat empty
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")

    #tester le chemin empty-(push-normal)*-push-full-(pop-normal)*-pop-empty
    def test_push_to_full(self):

        #tester divers choix de tailles
        for size in range(3, 10):
            stack = Stack(size, 20, 20)
            s = "|"

            #verification de l'etat initial
            self.assertTrue(stack.isEmpty())
            self.assertEqual(stack.size(), 0)
            self.assertFalse(stack.isFull())
            self.assertRaises(ValueError, stack.peek)
            self.assertEqual(str(stack),"|")

            #tester le push size fois
            for k in range(1, size):

                #tester la transition
                stack.push(k)
                s = "|"+str(k)+s

                #tester l'etat normal
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)
                self.assertEqual(str(stack), s)

            #tester la transition
            stack.push("last")

            #tester l'etat plein
            self.assertFalse(stack.isEmpty())
            self.assertEqual(stack.size(), size)
            self.assertTrue(stack.isFull())
            self.assertEqual(stack.peek(), "last")

            #tester la transition
            self.assertTrue(stack.pop(), "last")

            #tester le push size fois
            for k in range(size-1, 0, -1):

                #tester l'etat normal
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)

                #tester la transition
                self.assertEqual(stack.pop(), k)

        #tester l'etat empty
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")

    #tester le chemin empty-(push-normal)*-push-full-(push-full)*-(push-normal)*-push-full-(pop-normal)*-pop-empty
    def test_push_to_full_then_increment(self):

        #tester divers combinaisons de size, trial et increment
        for size in range(5, 10):
            for trial in range(5, 10):
                for increment in range(5, 10):
                    stack = Stack(size, trial, increment)
                    s = "|"

                    #verification de l'etat initial
                    self.assertTrue(stack.isEmpty())
                    self.assertEqual(stack.size(), 0)
                    self.assertFalse(stack.isFull())
                    self.assertRaises(ValueError, stack.peek)
                    self.assertEqual(str(stack),"|")

                    #tester le push size fois
                    for k in range(1, size):

                        #tester la transition
                        stack.push(k)
                        s = "|"+str(k)+s

                        #tester l'etat normal
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), k)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), k)
                        self.assertEqual(str(stack), s)

                    #tester la transition
                    stack.push("last")
                    s = "|last"+s

                    #tester l'etat plein
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size)
                    self.assertTrue(stack.isFull())
                    self.assertEqual(stack.peek(), "last")
                    self.assertEqual(str(stack), s)

                    #tester que stack va lancer une exception pour trial fois
                    for nb in range(1, trial):
                        self.assertRaises(ValueError, stack.push, "fail")

                        #tester que l'etat demeure plein
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size)
                        self.assertTrue(stack.isFull())
                        self.assertEqual(stack.peek(), "last")
                        self.assertEqual(str(stack), s)

                    #tester le dernier push errone avant que la taille de la pile augmente
                    self.assertRaises(ValueError, stack.push, "fail")

                    #tester l'etat normal
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size)
                    self.assertFalse(stack.isFull())
                    self.assertEqual(stack.peek(), "last")
                    self.assertEqual(str(stack), s)

                    #tester le push increment fois
                    for i in range(1, increment):

                        #tester la transition
                        stack.push(i)
                        s = "|"+str(i)+s

                        #tester l'etat normal
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size+i)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), i)
                        self.assertEqual(str(stack),s)

                    #tester la transition
                    stack.push("end")

                    #tester l'etat full une 2eme fois
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size+increment)
                    self.assertTrue(stack.isFull())
                    self.assertEqual(stack.peek(), "end")

                    #tester la transition
                    self.assertEqual(stack.pop(), "end")

                    #tester le pop increment fois
                    for i in range(increment-1, 0, -1):

                        #tester l'etat normal
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size+i)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), i)

                        #tester la transition
                        self.assertEqual(stack.pop(), i)

                    #tester la transition
                    self.assertTrue(stack.pop(), "last")

                    #tester le pop size fois
                    for k in range(size-1, 0, -1):

                        #tester l'etat normal
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), k)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), k)

                        #tester la transition
                        self.assertEqual(stack.pop(), k)

                #tester l'etat empty
                self.assertTrue(stack.isEmpty())
                self.assertEqual(stack.size(), 0)
                self.assertFalse(stack.isFull())
                self.assertRaises(ValueError, stack.peek)
                self.assertRaises(ValueError, stack.pop)
                self.assertEqual(str(stack),"|")

if __name__ == '__main__':
    unittest.main()