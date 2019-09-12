import sqlite3
import unittest
from unittest.mock import Mock
import os
from models import Contact
from DAOs import ContactDAO
from services import ContactService, AlreadyExistedItem, UndefinedID, NotExistedItem
from datetime import datetime

# To complete...
class TestContactService(unittest.TestCase):

    def setUp(self):
        self.contactDAO = Mock()
        self.contactService = ContactService(self.contactDAO)

    def test_when_contact_is_created_updated_should_be_True(self):
        self.contactDAO.add.return_value = 1 #Le mock retournera 1 lorsqu'on appellera la méthode add sur lui
        self.contactDAO.get_by_names.return_value = None
        contact = self.contactService.create_contact('Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')
        self.assertTrue(contact.updated)
    
    def test_when_contact_is_created_updated_date_should_be_now(self):
        self.contactDAO.add.return_value = 1 #Le mock retournera 1 lorsqu'on appellera la méthode add sur lui
        self.contactDAO.get_by_names.return_value = None
        contact = self.contactService.create_contact('Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')
        #approximation a zero decimales
        self.assertAlmostEqual(contact.updated_date, datetime.now().timestamp(),0)

    def test_when_contact_is_created_and_DAO_get_by_names_returns_contact_it_should_raise_AlreadyExistedItem(self):
        self.contactDAO.get_by_names.return_value = Contact(0, "Name", "lastName", '123-456-7891', "mail", True, "date")
        self.assertRaises(AlreadyExistedItem, self.contactService.create_contact,'Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')
    
    def test_when_contact_is_changed_updated_should_be_True(self):
        self.contactDAO.update.return_value = 1
        contact = self.contactService.update_contact(1,'Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')
        self.assertTrue(contact.updated)
    
    def test_when_contact_is_changed_updated_date_should_be_now(self):
        self.contactDAO.update.return_value = 1
        contact = self.contactService.update_contact(1,'Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')
        #approximation a zero decimales
        self.assertAlmostEqual(contact.updated_date, datetime.now().timestamp(),0)
    
    def test_when_contact_is_changed_and_DAO_update_returns_zero_it_should_raise_UndefinedID(self):
        self.contactDAO.update.return_value = 0
        self.assertRaises(UndefinedID, self.contactService.update_contact,1,'Houssem','Ben Braiek','123-456-7891','houssem.bb@gmail.com')

    def test_when_retrieve_contact_is_called_with_id_and_DAO_get_by_id_should_be_called(self):
        contact = Contact(0, "Name", "lastName", '123-456-7891', "mail", True, "date")
        self.contactDAO.get_by_id.return_value = contact
        self.assertEquals(self.contactService.retrieve_contact(1), contact)
        self.assertTrue(self.contactDAO.get_by_id.called)
    
    def test_when_retrieve_contact_is_called_with_names_and_DAO_get_by_names_should_be_called(self):
        contact = Contact(0, "Name", "lastName", '123-456-7891', "mail", True, "date")
        self.contactDAO.get_by_names.return_value = contact
        self.assertEquals(self.contactService.retrieve_contact(None, 'Name', 'lastName'), contact)
        self.assertTrue(self.contactDAO.get_by_names.called)

    def test_when_retrieve_contact_is_called_with_id_and_DAO_returns_None_it_should_raise_UndefinedID(self):
        self.contactDAO.get_by_id.return_value = None
        self.assertRaises(UndefinedID, self.contactService.retrieve_contact, 1)
    
    def test_when_retrieve_contact_is_called_with_names_and_DAO_returns_None_it_should_raise_NotExistedItem(self):
        self.contactDAO.get_by_names.return_value = None
        self.assertRaises(NotExistedItem, self.contactService.retrieve_contact, None, 'Name', 'lastName')

    def test_when_delete_contact_is_called_with_id_and_DAO_delete_by_id_should_be_called(self):
        self.contactDAO.delete_by_id.return_value = 1
        self.contactService.delete_contact(1)
        self.assertTrue(self.contactDAO.delete_by_id.called)
    
    def test_when_delete_contact_is_called_with_names_and_DAO_delete_by_names_should_be_called(self):
        self.contactDAO.delete_by_names.return_value = 1
        self.contactService.delete_contact(None, "Name", "lastName")
        self.assertTrue(self.contactDAO.delete_by_names.called)

    def test_when_delete_contact_is_called_with_id_and_DAO_delete_by_id_returns_zero_it_should_raise_UndefinedID(self):
        self.contactDAO.delete_by_id.return_value = 0
        self.assertRaises(UndefinedID, self.contactService.delete_contact, 1)
    
    def test_when_retrieve_contact_is_called_with_names_and_DAO_delete_by_names_returns_zero_it_should_raise_NotExistedItem(self):
        self.contactDAO.delete_by_names.return_value = 0
        self.assertRaises(NotExistedItem, self.contactService.delete_contact, None, "Name", "lastName")
    

    
if __name__ == '__main__':
    unittest.main()
    