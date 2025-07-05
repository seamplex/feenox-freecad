from PySide2 import QtWidgets

class BCEditorWidget(QtWidgets.QGroupBox):
    def __init__(self, bc_obj, parent=None):
        super().__init__(parent)
        self.bc = bc_obj
        self.setTitle(self.bc.name)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.face_list = QtWidgets.QListWidget()
        for obj, face in self.bc.face_refs:
            self.face_list.addItem(f"{obj.Name}.{face}")

        set_active_btn = QtWidgets.QPushButton("Set Active BC")
        set_active_btn.clicked.connect(lambda: self.parent().set_active_bc(self))
        layout.addWidget(set_active_btn)

        remove_face_btn = QtWidgets.QPushButton("Remove Selected Face")
        remove_face_btn.clicked.connect(self.remove_face)

        face_layout = QtWidgets.QVBoxLayout()
        face_layout.addWidget(QtWidgets.QLabel("Selected Faces:"))
        face_layout.addWidget(self.face_list)
        face_layout.addWidget(remove_face_btn)

        self.token_table = QtWidgets.QTableWidget(0, 2)
        self.token_table.setHorizontalHeaderLabels(["Property", "Expression"])

        add_token_btn = QtWidgets.QPushButton("+ Add Token")
        add_token_btn.clicked.connect(self.add_token_row)

        token_layout = QtWidgets.QVBoxLayout()
        token_layout.addWidget(QtWidgets.QLabel("Boundary Condition Tokens:"))
        token_layout.addWidget(self.token_table)
        token_layout.addWidget(add_token_btn)

        self.preview_box = QtWidgets.QPlainTextEdit()
        self.preview_box.setReadOnly(True)
        self.update_preview()

        update_btn = QtWidgets.QPushButton("Update Preview")
        update_btn.clicked.connect(self.apply_changes)

        layout.addLayout(face_layout)
        layout.addLayout(token_layout)
        layout.addWidget(QtWidgets.QLabel("Live Preview:"))
        layout.addWidget(self.preview_box)
        layout.addWidget(update_btn)

        self.setLayout(layout)

    def set_active_bc(self, widget):
        if self.active_observer:
            FreeCADGui.Selection.removeObserver(self.active_observer)
    
        self.active_observer = FaceSelectionObserver(widget.bc, widget)
        FreeCADGui.Selection.addObserver(self.active_observer)
        self.active_bc_widget = widget


    def remove_face(self):
        selected = self.face_list.currentItem()
        if selected:
            text = selected.text()
            obj_name, face_name = text.split('.')
            for obj, face in self.bc.face_refs:
                if obj.Name == obj_name and face == face_name:
                    self.bc.remove_face(obj, face)
                    break
            self.face_list.takeItem(self.face_list.currentRow())
            self.update_preview()

    def add_token_row(self):
        row = self.token_table.rowCount()
        self.token_table.insertRow(row)
        self.token_table.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
        self.token_table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))

    def apply_changes(self):
        self.bc.clear_tokens()
        for row in range(self.token_table.rowCount()):
            prop = self.token_table.item(row, 0).text()
            expr = self.token_table.item(row, 1).text()
            if prop and expr:
                self.bc.set_token(prop, expr)
        self.update_preview()

    def update_preview(self):
        self.preview_box.setPlainText(self.bc.write_fee_block())
