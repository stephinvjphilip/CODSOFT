import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTableView, QLineEdit, QDialog,
    QFormLayout, QMessageBox
)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt6.QtCore import Qt

class ContactDialog(QDialog):                 
    def __init__(self, title="Add Contact", contact=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        if contact:
            self.name_input.setText(contact[1])
            self.phone_input.setText(contact[2])
            self.email_input.setText(contact[3])
            self.address_input.setText(contact[4])

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Phone:", self.phone_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Address:", self.address_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_contact(self):
        return (self.name_input.text(),
                self.phone_input.text(),
                self.email_input.text(),
                self.address_input.text())

class ContactBook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Book")
        self.setGeometry(100, 100, 600, 400)

        self.connect_to_db()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name or phone number...")
        self.layout.addWidget(self.search_bar)

        self.contact_table = QTableView()
        self.layout.addWidget(self.contact_table)

        self.add_button = QPushButton("Add Contact")
        self.update_button = QPushButton("Update Contact")
        self.delete_button = QPushButton("Delete Contact")
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.add_button.clicked.connect(self.add_contact)
        self.update_button.clicked.connect(self.update_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.search_bar.textChanged.connect(self.search_contacts)

        self.load_contacts()

    def connect_to_db(self):
        db_path = 'contacts.db'
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_path)

        if not os.path.exists(db_path):
            if not db.open():
                QMessageBox.critical(self, "Database Error", "Unable to open database")
                return

            query = QSqlQuery()
            query.exec("""CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            address TEXT)""")
            db.close()
        else:
            if not db.open():
                QMessageBox.critical(self, "Database Error", "Unable to open database")
                return
            
    def load_contacts(self):
        self.model = QSqlTableModel()
        self.model.setTable('contacts')
        self.model.setSort(0, Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.contact_table.setModel(self.model)

    def add_contact(self):
        dialog = ContactDialog(title="Add Contact")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, phone, email, address = dialog.get_contact()

            query = QSqlQuery()
            query.exec("SELECT id FROM contacts ORDER BY id")
            
            used_ids = []
            while query.next():
                used_ids.append(query.value(0))
            
            new_id = 1
            for i in range(1, len(used_ids) + 2):
                if i not in used_ids:
                    new_id = i
                    break
                
            query.prepare("INSERT INTO contacts (id, name, phone, email, address) VALUES (?, ?, ?, ?, ?)")
            query.addBindValue(new_id)
            query.addBindValue(name)
            query.addBindValue(phone)
            query.addBindValue(email)
            query.addBindValue(address)

            if not query.exec():
                QMessageBox.critical(self, "Database Error", "Error adding contact")

            self.load_contacts()

    def update_contact(self):
        selected_row = self.contact_table.currentIndex().row()
        
        if selected_row >= 0:
            contact_id = self.model.index(selected_row, 0).data()
            current_contact = (
                contact_id,
                self.model.index(selected_row, 1).data(),
                self.model.index(selected_row, 2).data(),
                self.model.index(selected_row, 3).data(),
                self.model.index(selected_row, 4).data()
            )

            dialog = ContactDialog(title="Update Contact", contact=current_contact)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                name, phone, email, address = dialog.get_contact()

                query = QSqlQuery()
                query.prepare("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?")
                query.addBindValue(name)
                query.addBindValue(phone)
                query.addBindValue(email)
                query.addBindValue(address)
                query.addBindValue(contact_id)

                if not query.exec():
                    QMessageBox.critical(self, "Database Error", "Error updating contact")

                self.load_contacts()

    def delete_contact(self):
        selected_row = self.contact_table.currentIndex().row()
        
        if selected_row >= 0:
            contact_id = self.model.index(selected_row, 0).data()
            
            query = QSqlQuery()
            query.prepare("DELETE FROM contacts WHERE id=?")
            query.addBindValue(contact_id)

            if not query.exec():
                QMessageBox.critical(self, "Database Error", "Error deleting contact")

            self.load_contacts()

    def search_contacts(self):
        search_text = self.search_bar.text()
        self.model.setFilter(f"name LIKE '%{search_text}%' OR phone LIKE '%{search_text}%'")
        self.model.select()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = ContactBook()
    window.show()
    
    sys.exit(app.exec())
