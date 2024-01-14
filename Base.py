from Base_UI import Ui_MainWindow
from PyQt5.Qt import QApplication, Qt
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel
import sqlite3
from Add_UI import Ui_Add_component
from Change_UI import Ui_Change_component
from Projects_UI import Ui_Projects
from Add_elements_UI import Ui_Add_Element
from Change_elements_UI import Ui_Change_Element
from Cases_UI import Ui_Cases
import configparser
import os

headers = {
    'Резисторы': ('ID', 'Корпус', 'Номинал', 'Допуск', 'Адрес', 'Количество'),
    'Конденсаторы': ('ID', 'Корпус', 'Номинал', 'Допуск', 'Материал', 'Адрес', 'Количество'),
    'Диоды': ('ID', 'Корпус', 'Номинал', 'Адрес', 'Количество'),
    'Транзисторы': ('ID', 'Корпус', 'Номинал', 'Адрес', 'Количество'),
    'Микросхемы': ('ID', 'Корпус', 'Номинал', 'Адрес', 'Количество'),
    'Дроссели': ('ID', 'Корпус', 'Номинал', 'Допуск', 'Адрес', 'Количество'),
    'Разъемы': ('ID', 'Номинал', 'Адрес', 'Количество'),
    'Прочее': ('ID', 'Номинал', 'Адрес', 'Количество')
}
elements_headers = {
    'Резисторы': ('ID', 'Корпус', 'Номинал', 'Допуск'),
    'Конденсаторы': ('ID', 'Корпус', 'Номинал', 'Допуск', 'Материал'),
    'Диоды': ('ID', 'Корпус', 'Номинал'),
    'Транзисторы': ('ID', 'Корпус', 'Номинал'),
    'Микросхемы': ('ID', 'Корпус', 'Номинал'),
    'Дроссели': ('ID', 'Корпус', 'Номинал', 'Допуск'),
    'Разъемы': ('ID', 'Номинал'),
    'Прочее': ('ID', 'Номинал')
}

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cases = Cases()
        self.add_components = AddComponent()
        self.change_components = ChangeComponent()
        self.add_elements = AddElements()
        self.change_elements = ChangeElements()
        self.projects = Projects()
        self.resistors_data = []
        self.capacitors_data = []
        self.diodes_data = []
        self.transistors_data = []
        self.microschemes_data = []
        self.drossels_data = []
        self.connectors_data = []
        self.other_data = []
        self.resistors_in_model = TableModel(headers['Резисторы'], self.resistors_data)
        self.resistors_model = QSortFilterProxyModel()
        self.resistors_model.setSourceModel(self.resistors_in_model)
        self.capacitors_in_model = TableModel(headers['Конденсаторы'], self.capacitors_data)
        self.capacitors_model = QSortFilterProxyModel()
        self.capacitors_model.setSourceModel(self.capacitors_in_model)
        self.diodes_in_model = TableModel(headers['Диоды'], self.diodes_data)
        self.diodes_model = QSortFilterProxyModel()
        self.diodes_model.setSourceModel(self.diodes_in_model)
        self.transistors_in_model = TableModel(headers['Транзисторы'], self.transistors_data)
        self.transistors_model = QSortFilterProxyModel()
        self.transistors_model.setSourceModel(self.transistors_in_model)
        self.microschemes_in_model = TableModel(headers['Микросхемы'], self.microschemes_data)
        self.microschemes_model = QSortFilterProxyModel()
        self.microschemes_model.setSourceModel(self.microschemes_in_model)
        self.drossels_in_model = TableModel(headers['Дроссели'], self.drossels_data)
        self.drossels_model = QSortFilterProxyModel()
        self.drossels_model.setSourceModel(self.drossels_in_model)
        self.connectors_in_model = TableModel(headers['Разъемы'], self.connectors_data)
        self.connectors_model = QSortFilterProxyModel()
        self.connectors_model.setSourceModel(self.connectors_in_model)
        self.other_in_model = TableModel(headers['Прочее'], self.other_data)
        self.other_model = QSortFilterProxyModel()
        self.other_model.setSourceModel(self.other_in_model)

        self.projects_data = []
        self.cases_data = []
        self.mount_data = []
        self.statistic_data = []
        self.report_data = []
        self.projects_in_model = TableModel(('ID', 'Проект'), self.projects_data)
        self.projects_model = QSortFilterProxyModel()
        self.projects_model.setSourceModel(self.projects_in_model)
        self.cases_in_model = TableModel(('ID', 'Группа', 'Корпус'), self.cases_data)
        self.cases_model = QSortFilterProxyModel()
        self.cases_model.setSourceModel(self.cases_in_model)
        self.mount_in_model = TableModel(('Обозначение', 'Корпус', 'Номинал', 'Допуск', 'Материал', 'Адрес', 'Очередь'),
                                         self.mount_data)
        self.mount_model = QSortFilterProxyModel()
        self.mount_model.setSourceModel(self.mount_in_model)
        self.statistic_in_model = TableModel(('Группа', 'Корпус', 'Номинал', 'Допуск', 'Материал', 'Количество'),
                                             self.statistic_data)
        self.statistic_model = QSortFilterProxyModel()
        self.statistic_model.setSourceModel(self.statistic_in_model)
        self.report_in_model = TableModel(('Группа', 'Корпус', 'Номинал', 'Допуск', 'Материал', 'В наличии',
                                           'Требуется', 'Докупить'), self.report_data)
        self.report_model = QSortFilterProxyModel()
        self.report_model.setSourceModel(self.report_in_model)
        self.change_ui_forms = (self.change_components.casing_box, self.change_components.lineEdit_2,
                                self.change_components.spinBox_2, self.change_components.lineEdit_3,
                                self.change_components.lineEdit_4, self.change_components.spinBox)
        self.fields = (
            ('Корпус', 'Номинал', 'Допуск', 'Адрес', 'Количество'),
            ('Корпус', 'Номинал', 'Допуск', 'Материал', 'Адрес', 'Количество'),
            ('Корпус', 'Номинал', 'Адрес', 'Количество'),
            ('Корпус', 'Номинал', 'Адрес', 'Количество'),
            ('Корпус', 'Номинал', 'Адрес', 'Количество'),
            ('Корпус', 'Номинал', 'Допуск', 'Адрес', 'Количество'),
            ('Номинал', 'Адрес', 'Количество'),
            ('Номинал', 'Адрес', 'Количество')
        )
        self.filling_columns = (
            'id, case_id, nominal, deviation, address, quantity',
            'id, case_id, nominal, deviation, material, address, quantity',
            'id, case_id, nominal, address, quantity',
            'id, case_id, nominal, address, quantity',
            'id, case_id, nominal, address, quantity',
            'id, case_id, nominal, deviation, address, quantity',
            'id, nominal, address, quantity',
            'id, nominal, address, quantity'
        )
        self.columns = (
            'type, case_id, nominal, deviation, address, quantity',
            'type, case_id, nominal, deviation, material, address, quantity',
            'type, case_id, nominal, address, quantity',
            'type, case_id, nominal, address, quantity',
            'type, case_id, nominal, address, quantity',
            'type, case_id, nominal, deviation, address, quantity',
            'type, nominal, address, quantity',
            'type, nominal, address, quantity'
        )
        self.components_cases = ('0805', '0805', 'SOT-23', 'SOT-23', 'DIP-8', '0805')
        self.checking_fields = (
            'case_id, nominal, deviation', 'case_id, nominal, deviation, material', 'case_id, nominal',
            'case_id, nominal', 'case_id, nominal', 'case_id, nominal, deviation', 'nominal', 'nominal')
        self.tables = (self.resistors, self.capacitors, self.diodes, self.transistors, self.microschemes,
                       self.drossels, self.connectors, self.other)
        self.cases_groups = ('Резисторы', 'Конденсаторы', 'Диоды', 'Транзисторы', 'Микросхемы', 'Дроссели')
        self.add_ui_disabled_fields = (self.add_components.cases_box, self.add_components.spinBox_2,
                                       self.add_components.lineEdit_4)
        self.add_ui_enabled_fields = ((self.add_components.cases_box, self.add_components.spinBox_2),
                                      (self.add_components.cases_box, self.add_components.spinBox_2,
                                       self.add_components.lineEdit_4), (self.add_components.cases_box,),
                                      (self.add_components.cases_box,), (self.add_components.cases_box,),
                                      (self.add_components.cases_box, self.add_components.spinBox_2),
                                      (self.add_components.lineEdit_2,), (self.add_components.lineEdit_2,))
        self.change_ui_enabled_fields = ((self.change_components.casing_box, self.change_components.lineEdit_2,
                                          self.change_components.spinBox_2, self.change_components.lineEdit_4,
                                          self.change_components.spinBox), (self.change_components.casing_box,
                                                                            self.change_components.lineEdit_2,
                                                                            self.change_components.spinBox_2,
                                                                            self.change_components.lineEdit_3,
                                                                            self.change_components.lineEdit_4,
                                                                            self.change_components.spinBox),
                                         (self.change_components.casing_box, self.change_components.lineEdit_2,
                                          self.change_components.lineEdit_4, self.change_components.spinBox),
                                         (self.change_components.casing_box, self.change_components.lineEdit_2,
                                          self.change_components.lineEdit_4, self.change_components.spinBox),
                                         (self.change_components.casing_box, self.change_components.lineEdit_2,
                                          self.change_components.lineEdit_4, self.change_components.spinBox),
                                         (self.change_components.casing_box, self.change_components.lineEdit_2,
                                          self.change_components.spinBox_2, self.change_components.lineEdit_4,
                                          self.change_components.spinBox), (self.change_components.lineEdit_2,
                                                                            self.change_components.lineEdit_4,
                                                                            self.change_components.spinBox),
                                         (self.change_components.lineEdit_2, self.change_components.lineEdit_4,
                                          self.change_components.spinBox))
        self.change_ui_disabled_fields = (self.change_components.casing_box, self.change_components.spinBox_2,
                                          self.change_components.lineEdit_3)
        self.models = {
            self.resistors: self.resistors_model, self.capacitors: self.capacitors_model,
            self.diodes: self.diodes_model, self.transistors: self.transistors_model,
            self.microschemes: self.microschemes_model, self.drossels: self.drossels_model,
            self.connectors: self.connectors_model, self.other: self.other_model
        }
        self.in_models = (
            self.resistors_in_model, self.capacitors_in_model, self.diodes_in_model, self.transistors_in_model,
            self.microschemes_in_model, self.drossels_in_model, self.connectors_in_model, self.other_in_model
        )
        for table in self.models:
            table.setModel(self.models[table])
            table.setSortingEnabled(True)
            table.sortByColumn(0, Qt.AscendingOrder)

        self.projects.tableView.setModel(self.projects_model)
        self.projects.tableView.setSortingEnabled(True)
        self.projects.tableView.sortByColumn(1, Qt.AscendingOrder)
        self.cases.tableView.setModel(self.cases_model)
        self.cases.tableView.setSortingEnabled(True)
        self.cases.tableView.sortByColumn(1, Qt.AscendingOrder)
        self.components.setModel(self.mount_model)
        self.components.setSortingEnabled(True)
        self.components.sortByColumn(6, Qt.AscendingOrder)
        self.statistic.setModel(self.statistic_model)
        self.statistic.setSortingEnabled(True)
        self.statistic.sortByColumn(0, Qt.AscendingOrder)
        self.statistic_2.setModel(self.report_model)
        self.statistic_2.setSortingEnabled(True)
        self.statistic_2.sortByColumn(0, Qt.AscendingOrder)
        self.groups = (
            'Резисторы', 'Конденсаторы', 'Диоды', 'Транзисторы', 'Микросхемы', 'Дроссели', 'Разъемы', 'Прочее'
        )
        self.data_groups = (
            self.resistors_data, self.capacitors_data, self.diodes_data, self.transistors_data, self.microschemes_data,
            self.drossels_data, self.connectors_data, self.other_data
        )
        self.actions_enable()
        self.add_action.triggered.connect(self.add_component)
        self.actionToolBar.triggered.connect(self.set_toolbar)
        self.tabWidget_3.currentChanged.connect(self.actions_enable)
        self.tabWidget.currentChanged.connect(self.actions_enable)
        self.comboBox.currentIndexChanged.connect(self.components_filling)
        self.comboBox.currentIndexChanged.connect(self.statistic_table)
        self.config = configparser.RawConfigParser()
        self.conn = sqlite3.connect('Details.db')
        self.cursor = self.conn.cursor()
        self.filling()
        self.projects_filling()
        self.project_list()
        self.components_filling()
        self.statistic_table()
        self.available_components()
        # self.ref_list()
        self.cases.comboBox.addItems(self.cases_groups)
        self.cases_filling()
        self.comboBox.currentIndexChanged.connect(self.ref_list)
        self.add_elements.comboBox.addItems(self.groups)
        self.change_elements.comboBox.addItems(self.groups)
        self.set_toolbar()
        self.comboBox.currentIndexChanged.connect(self.available_components)
        self.add_action.triggered.connect(self.add_component)
        self.action_2.triggered.connect(lambda: self.projects.show())
        self.cases_action.triggered.connect(lambda: self.cases.show())
        self.add_elemetn_action.triggered.connect(self.add_element)
        self.spinBox_2.valueChanged.connect(self.available_components)
        self.del_action.triggered.connect(self.del_qwestion)
        self.up_action.triggered.connect(self.move_up)
        self.down_action.triggered.connect(self.move_down)
        self.components.doubleClicked.connect(self.change_element)
        for component_table in self.tables:
            component_table.doubleClicked.connect(self.change_component)
        self.change_elements.buttonBox.clicked.connect(self.change_element_action)
        self.change_components.buttonBox.accepted.connect(self.save_changed_component)
        self.change_components.radioButton.clicked.connect(self.change_ui_set_enable)
        self.change_components.radioButton_2.clicked.connect(self.change_ui_set_enable)
        self.change_components.radioButton_4.clicked.connect(self.change_ui_set_enable)
        self.add_elements.buttonBox.clicked.connect(self.add_element_action)
        self.add_elements.comboBox.currentIndexChanged.connect(lambda: self.elements_list(self.add_elements))
        # self.change_elements.ref_box.currentIndexChanged.connect(self.set_components_values)
        self.change_elements.comboBox.currentIndexChanged.connect(lambda: self.elements_list(self.change_elements))
        self.del_element_action.triggered.connect(self.del_element_qwestion)
        self.print_action.triggered.connect(self.handlePreview)
        self.projects.add_btn.clicked.connect(self.add_project)
        self.projects.del_btn.clicked.connect(self.del_project_qwestion)
        self.projects.close_btn.clicked.connect(lambda: self.projects.close())
        self.cases.comboBox.currentIndexChanged.connect(self.cases_filling)
        self.cases.add_btn.clicked.connect(self.add_case)
        self.cases.del_btn.clicked.connect(self.del_case_qwestion)
        self.cases.close_btn.clicked.connect(lambda: self.cases.close())
        self.pushButton.clicked.connect(self.unload_qwestion)
        if not os.path.isfile('settings.ini'):
            self.make_config()
        self.tabWidget.setCurrentIndex(int(self.setconfig()[0]))
        self.tabWidget_2.setCurrentIndex(int(self.setconfig()[1]))
        self.tabWidget_3.setCurrentIndex(int(self.setconfig()[3]))
        self.comboBox.setCurrentIndex(int(self.setconfig()[2]))
        self.actionToolBar.setChecked(True) if self.setconfig()[4] == 'ON' else self.actionToolBar.setChecked(False)
        self.about_action.triggered.connect(self.show_about)
        self.help_action.triggered.connect(self.show_help)
        self.add_components.buttonBox.accepted.connect(self.save_component)

    def make_config(self):
        self.config.add_section('INDEX')
        self.config.set('INDEX', 'index_tab_0', '0')
        self.config.set('INDEX', 'index_tab_1', '0')
        self.config.set('INDEX', 'index_tab_2', '0')
        self.config.set('INDEX', 'combo_index', '0')
        self.config.add_section('TOOLBAR')
        self.config.set('TOOLBAR', 'status', 'ON')
        with open('settings.ini', 'w') as f:
            self.config.write(f)

    def setconfig(self):
        self.config.read('settings.ini')
        index_tab_0 = self.config.get('INDEX', 'index_tab_0')
        index_tab_1 = self.config.get('INDEX', 'index_tab_1')
        index_tab_2 = self.config.get('INDEX', 'index_tab_2')
        combo_index = self.config.get('INDEX', 'combo_index')
        toolbar = self.config.get('TOOLBAR', 'status')
        return index_tab_0, index_tab_1, combo_index, index_tab_2, toolbar

    @staticmethod
    def show_error(errormessage):
        error = QMessageBox()
        error.setWindowTitle("Ошибка!")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Logo.png"))
        error.setWindowIcon(icon)
        error.setText(errormessage)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    def del_qwestion(self):
        table = self.current_table()
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите компонент!')
            return
        qwest = QMessageBox()
        qwest.setWindowTitle("Удалить компонент")
        qwest.setText("Вы уверны, что хотите удалить компонент?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.del_qwestion_action)
        qwest.exec_()

    def del_qwestion_action(self, btn):
        if btn.text() in ['OK', '&OK']:
            self.del_component()

    def filling(self):
        with self.conn:
            self.conn.execute("""
                        CREATE TABLE IF NOT EXISTS components (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            type VARCHAR,
                            case_id VARCHAR,
                            nominal VARCHAR,
                            deviation int,
                            material VARCHAR DEFAULT '-',
                            address VARCHAR default '-',
                            quantity INTEGER
                        );
                    """)
            self.conn.execute(''
                              'create table if not exists cases ('
                              'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                              'type varchar,'
                              'casing varchar)'
                              )
            self.conn.execute(''
                              'create table if not exists projects ('
                              'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                              'project_name varchar)'
                              )
            for i, group in enumerate(self.groups):
                data = self.data_groups[i]
                in_model = self.in_models[i]
                columns_list = self.filling_columns[i]
                source_data = self.conn.execute(f"select {columns_list} from components where "
                                                f"type = '{group}'").fetchall()
                for row in source_data:
                    data.append(row)
                in_model.setItems(data)

    def projects_filling(self):
        self.projects_data.clear()
        with self.conn:
            data = self.conn.execute('select * from projects')
            for row in data:
                self.projects_data.append(row)
            self.projects_in_model.setItems(self.projects_data)

    def cases_filling(self):
        group = self.cases.comboBox.currentText()
        self.cases_data.clear()
        with self.conn:
            data = self.conn.execute(f'select id, type, casing from cases where type = "{group}"')
            for row in data:
                self.cases_data.append(row)
        self.cases_in_model.setItems(self.cases_data)

    def components_filling(self):
        project = self.comboBox.currentText()
        if project != '':
            self.mount_data.clear()
            table_components = f'{project}_components'
            with self.conn:
                data = self.conn.execute(
                    f'select ref_des, case_id, nominal, deviation, material, address, priority from "{table_components}" '
                    f'join components on "{table_components}".element_id = components.id'
                )
                for row in data:
                    self.mount_data.append(row)
                self.mount_in_model.setItems(self.mount_data)
            # self.ref_list()
            # self.change_elements.ref_box.clear()
            # for i in ref:
            #     self.change_elements.ref_box.addItem(i[0])
            # self.change_elements.ref_box.setCurrentIndex(0)

    def add_component(self):
        self.clear_fields()
        index = self.tabWidget_2.currentIndex()
        if index < 6:
            caselist = self.case_list(self.groups[index])
            it = sorted(caselist)
            self.add_components.cases_box.addItems(it)
        disabled = self.add_ui_disabled_fields
        enabled = self.add_ui_enabled_fields[index]
        self.set_form_fields(disabled, enabled)
        self.add_components.show()

    def save_component(self):
        index = self.tabWidget_2.currentIndex()
        group = self.groups[index]
        case = str(self.add_components.cases_box.currentText())
        nominal = str(self.add_components.lineEdit_2.text())
        addr = str(self.add_components.lineEdit_3.text())
        quantity = self.add_components.spinBox.value()
        limit = self.add_components.spinBox_2.value()
        material = self.add_components.lineEdit_4.text()
        checking_data = {0: (case, nominal, limit),
                         1: (case, nominal, limit, material),
                         2: (case, nominal),
                         3: (case, nominal),
                         4: (case, nominal),
                         5: (case, nominal, limit),
                         6: (nominal,),
                         7: (nominal,)}
        values = {0: (group, case, nominal, limit, addr, quantity),
                  1: (group, case, nominal, limit, material, addr, quantity),
                  2: (group, case, nominal, addr, quantity),
                  3: (group, case, nominal, addr, quantity),
                  4: (group, case, nominal, addr, quantity),
                  5: (group, case, nominal, limit, addr, quantity),
                  6: (group, nominal, addr, quantity),
                  7: (group, nominal, addr, quantity)}
        check = self.checking_fields[index]
        col = self.columns[index]
        verify_data = self.checklist(check, group, 0)
        for i in verify_data:
            if i == checking_data[index]:
                self.show_error('Такой компонент уже имеется в базе!')
                return
        with self.conn:
            self.cursor.execute(f'insert into components ({col}) values{values[index]}')
        self.refresh_data(index)
        self.elements_list(self.add_elements)
        self.elements_list(self.change_elements)

    def change_component(self):
        self.change_components.casing_box.clear()
        index = self.tabWidget_2.currentIndex()
        model = self.tables[index].model()
        if index < 6:
            self.change_components.casing_box.addItems(self.case_list(self.cases_groups[index]))
        disabled = self.change_ui_disabled_fields
        enabled = self.change_ui_enabled_fields[index]
        self.set_form_fields(disabled, enabled)
        self.change_ui_set_enable()
        fields_values = {'Корпус': (self.change_components.casing_box.setCurrentText, str),
                         'Номинал': (self.change_components.lineEdit_2.setText, str),
                         'Допуск': (self.change_components.spinBox_2.setValue, int),
                         'Материал': (self.change_components.lineEdit_3.setText, str),
                         'Адрес': (self.change_components.lineEdit_4.setText, str),
                         'Количество': (self.change_components.spinBox.setValue, int)}
        table = self.current_table()
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите компонент!')
            return
        col = self.fields[index]

        for i, item in enumerate(col):
            target = fields_values[item][0]
            prefix = fields_values[item][1]
            model_index = model.index(row, i + 1)
            model_item = model.data(model_index)
            target(prefix(model_item))

        self.change_components.show()

    def del_component(self):
        index = self.tabWidget_2.currentIndex()
        table = self.current_table()
        row = table.currentIndex().row()
        model = table.model()
        id_index = model.index(row, 0)
        component_id = model.data(id_index)
        with self.conn:
            self.cursor.execute(f'DELETE from components WHERE id = "{component_id}"')
        self.elements_list(self.add_elements)
        self.elements_list(self.change_elements)
        self.refresh_data(index)

    def set_toolbar(self):
        if self.actionToolBar.isChecked():
            self.toolBar.show()
        else:
            self.toolBar.close()
            self.actionToolBar.setChecked(False)

        if not self.actionToolBar.isChecked():
            self.toolBar.close()
        else:
            self.toolBar.show()
            self.actionToolBar.setChecked(True)

    def actions_enable(self):
        self.print_action.setEnabled(True) if self.tabWidget.currentIndex() == 0\
            else self.print_action.setEnabled(False)
        if self.tabWidget.currentIndex() == 0 and self.tabWidget_3.currentIndex() == 0:
            self.add_elemetn_action.setEnabled(True)
            self.del_element_action.setEnabled(True)
            self.down_action.setEnabled(True)
            self.up_action.setEnabled(True)
        else:
            self.add_elemetn_action.setEnabled(False)
            self.del_element_action.setEnabled(False)
            self.down_action.setEnabled(False)
            self.up_action.setEnabled(False)

        if self.tabWidget.currentIndex() == 1:
            self.add_action.setEnabled(True)
            self.del_action.setEnabled(True)
        else:
            self.add_action.setEnabled(False)
            self.del_action.setEnabled(False)

    def add_element(self):
        self.elements_list(self.add_elements)
        self.add_elements.show()

    def add_element_action(self, btn):
        if btn.text() in ['Apply']:
            self.save_element()
        else:
            if btn.text() in ['OK']:
                self.save_element()
                self.add_elements.close()
            self.add_elements.close()

    def save_element(self):
        group = self.add_elements.comboBox.currentText()
        group_index = self.add_elements.comboBox_2.currentIndex()
        ref = self.add_elements.lineEdit.text()
        if ref == '':
            self.show_error('Введите обозначение элемента')
            return
        count = self.increment()
        project_name = self.comboBox.currentText()
        table_components = f'{project_name}_components'
        element_id = self.id_list(group)[group_index][0]
        with self.conn:
            check = self.cursor.execute(f'select * from "{table_components}" where ref_des = "{ref}"')

            if check.fetchone() is None:
                self.cursor.execute(f'INSERT INTO "{table_components}" (ref_des, priority, element_id)'
                                    f'values("{ref}", "{count}", "{element_id}")')
                self.components_filling()
                self.available_components()
                self.statistic_table()
            else:
                self.show_error('Такой элемент уже имеется в проекте')
                return

    def change_element(self):
        self.ref_list()
        table = self.components
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите элемент!')
            return
        model = table.model()
        ref_index = model.index(row, 0)
        ref_des = model.data(ref_index)
        group = self.element_data(ref_des)[0]
        element = self.element_data(ref_des)[1]
        self.change_elements.ref_box.setCurrentText(ref_des)
        # print(self.change_elements.ref_box.currentText())
        self.change_elements.comboBox.setCurrentText(group)
        self.elements_list(self.change_elements)
        self.change_elements.comboBox_2.setCurrentText(str(element))
        # self.change_elements.ref_box.currentIndexChanged.connect(self.set_components_values)
        self.change_elements.show()

    def save_changed_component(self):
        index = self.tabWidget_2.currentIndex()
        group = self.groups[index]
        quantity = self.change_components.spinBox.value()
        table = self.tables[index]
        row = table.currentIndex().row()
        model = table.model()
        model_index = model.index(row, 0)
        component_id = model.data(model_index)
        if self.change_components.radioButton.isChecked():
            verifing_fields = self.checking_fields[index]
            case = self.change_components.casing_box.currentText()
            nominal = self.change_components.lineEdit_2.text()
            limit = self.change_components.spinBox_2.value()
            material = self.change_components.lineEdit_3.text()
            addr = self.change_components.lineEdit_4.text()
            fields_values = {'case_id': case, 'nominal': nominal, 'deviation': limit, 'material': material,
                             'address': addr,
                             'quantity': quantity}
            changing_fields = (('case_id', 'nominal', 'deviation', 'address', 'quantity'),
                               ('case_id', 'nominal', 'deviation', 'material', 'address', 'quantity'),
                               ('case_id', 'nominal', 'address', 'quantity'),
                               ('case_id', 'nominal', 'address', 'quantity'),
                               ('case_id', 'nominal', 'address', 'quantity'),
                               ('case_id', 'nominal', 'deviation', 'address', 'quantity'),
                               ('nominal', 'address', 'quantity'),
                               ('nominal', 'address', 'quantity'))

            checking_values = {0: (case, nominal, limit),
                               1: (case, nominal, limit, material),
                               2: (case, nominal),
                               3: (case, nominal),
                               4: (case, nominal),
                               5: (case, nominal, limit),
                               6: (nominal,),
                               7: (nominal,)}

            checking_data = self.checklist(verifing_fields, group, component_id)

            if checking_values[index] in checking_data:
                self.show_error('Такой компонент уже имеется в базе!')
                return

            changed = changing_fields[index]

            with self.conn:
                for item in changed:
                    insert = f'{item} = "{fields_values[item]}"'
                    self.cursor.execute(f'update components set {insert} where id = "{component_id}"')

        if self.change_components.radioButton_2.isChecked():
            with self.conn:
                component_quantity = self.cursor.execute(
                    f'select quantity from components where id = "{component_id}"').fetchone()[0]
                diffrent = component_quantity - self.change_components.spinBox_3.value()
                quantity_new = 0 if diffrent < 0 else diffrent
                self.cursor.execute(f'update components set quantity = {quantity_new} where id = "{component_id}"')
                self.report('Выгружено', self.change_components.spinBox_3.value())

        if self.change_components.radioButton_4.isChecked():
            with self.conn:
                component_quantity = self.cursor.execute(
                    f'select quantity from components where id = "{component_id}"').fetchone()[0]
                quantity_new = component_quantity + self.change_components.spinBox_4.value()
                self.cursor.execute(f'update components set quantity = {quantity_new} where id = "{component_id}"')
                self.report('Добавлено', self.change_components.spinBox_4.value())

        self.components_filling()
        self.refresh_data(index)
        self.available_components()
        self.statistic_table()

    def refresh_data(self, index):
        group = self.groups[index]
        columns_list = self.filling_columns[index]
        model = self.in_models[index]
        data = self.data_groups[index]
        data.clear()
        with self.conn:
            source_data = self.conn.execute(f"select {columns_list} from components where type = '{group}'").fetchall()
            for row in source_data:
                data.append(row)
            model.setItems(data)

    def change_element_action(self, btn):
        if btn.text() in ['Apply']:
            self.save_changed_element()
        else:
            if btn.text() in ['OK']:
                self.save_changed_element()
                self.change_elements.close()
            self.change_elements.close()

    def save_changed_element(self):
        group = self.change_elements.comboBox.currentText()
        group_index = self.change_elements.comboBox_2.currentIndex()
        project_name = self.comboBox.currentText()
        ref = self.change_elements.ref_box.currentText()
        element_id = self.id_list(group)[group_index][0]
        table_components = f'{project_name}_components'
        with self.conn:
            self.cursor.execute(f'update "{table_components}" set element_id = "{element_id}" where ref_des = "{ref}"')
        self.components_filling()
        # self.elements_list(self.add_elements)
        # self.elements_list(self.change_elements)
        self.available_components()
        self.statistic_table()

    def increment(self):
        project = self.comboBox.currentText()
        table = f'{project}_components'
        with self.conn:
            counts = self.cursor.execute(f'select priority from "{table}"').fetchall()
            count_list = []
            for i in counts:
                count_list.append(i[0])
            count = 1 if count_list == [] else max(count_list) + 1
        return count

    def id_list(self, group):
        with self.conn:
            data = self.cursor.execute(f'select id from components where type = "{group}"')
            return data.fetchall()

    def project_list(self):
        with self.conn:
            projects_names = self.conn.execute('select * from projects')
            for i in projects_names:
                self.comboBox.addItem(i[1])
        self.comboBox.setCurrentIndex(int(self.setconfig()[2]))

    def elements_list(self, target):
        group = target.comboBox.currentText()
        index = target.comboBox.currentIndex()
        values = self.checking_fields[index]
        target.comboBox_2.clear()
        with self.conn:
            elements = self.conn.execute(f'select {values} from components where type = "{group}"')
            list = []
            for i in elements:

                list.append(str(i))
            target.comboBox_2.addItems(list)
        # target.comboBox_2.setCurrentIndex(0)

    def statistic_table(self):
        elements_table = f'{self.comboBox.currentText()}_components'
        if elements_table != '_components':
            self.statistic_data.clear()
            with self.conn:
                data = self.cursor.execute(
                    f'select type, case_id, nominal, deviation, material from "{elements_table}" join components on '
                    f'"{elements_table}".element_id = components.id').fetchall()
                elements = []
                [elements.append(i) for i in data if i not in elements]
                for row in elements:
                    new_row = []
                    for column in row:
                        new_row.append(column)
                    new_row.append(data.count(row))
                    self.statistic_data.append(new_row)
                self.statistic_in_model.setItems(self.statistic_data)

    def available_components(self):
        elements_table = f'{self.comboBox.currentText()}_components'
        if elements_table != '_components':
            self.report_data.clear()
            k = self.spinBox_2.value()
            with self.conn:
                data = self.cursor.execute(
                    f'select type, case_id, nominal, deviation, material, quantity from "{elements_table}" '
                    f'join components on "{elements_table}".element_id = components.id').fetchall()
                elements = []
                [elements.append(i) for i in data if i not in elements]
                for row in elements:
                    new_row = []
                    for column in (row):
                        new_row.append(column)
                    quantity = row[5]
                    complect = data.count(row)
                    # new_row.append(complect)
                    req = complect * k
                    new_row.append(req)
                    diff = quantity - req
                    res = 0 if diff > 0 else abs(diff)
                    new_row.append(res)
                    self.report_data.append(new_row)
                self.report_in_model.setItems(self.report_data)

    def set_form_fields(self, disabled, enabled):
        for i in disabled:
            i.setEnabled(False)
        for j in enabled:
            j.setEnabled(True)

    def clear_fields(self):
        self.add_components.cases_box.clear()
        self.add_components.lineEdit_2.clear()
        self.add_components.lineEdit_3.clear()
        self.add_components.lineEdit_4.clear()
        self.add_components.spinBox.setValue(0)
        self.add_components.spinBox_2.setValue(0)

    def case_list(self, group):
        data_list = []
        with self.conn:
            data = self.conn.execute(f'select casing from cases where type = "{group}"')
            for item in data:
                data_list.append(item[0])
        out_list = sorted(data_list)
        return out_list

    def projects_control(self):
        self.projects.show()

    def current_table(self):
        index = self.tabWidget_2.currentIndex()
        table = self.tables[index]
        return table

    def checklist(self, fields, group, component_id):
        with self.conn:
            data = self.cursor.execute(
                f'select {fields} from components where type = "{group}" and id is not {component_id}'
            )
            return data

    def ref_list(self):
        project = self.comboBox.currentText()
        table = f'{project}_components'
        with self.conn:
            data = self.cursor.execute(f'select ref_des from "{table}"')
            self.change_elements.ref_box.clear()
            for i in data:
                self.change_elements.ref_box.addItem(i[0])
            # print(self.change_elements.ref_box.currentText())
            # return data.fetchall()

    def element_data(self, ref_des):
        project = self.comboBox.currentText()
        table = f'{project}_components'
        with self.conn:
            element_id = self.cursor.execute(
                f'select element_id from "{table}" where ref_des = "{ref_des}"').fetchone()[0]
            group = self.cursor.execute(f'select type from components where id = "{element_id}"').fetchone()[0]
            index = self.groups.index(group)
            fields_list = self.checking_fields[index]
            component = self.cursor.execute(
                f'select {fields_list} from components where id = "{element_id}"').fetchone()
        return group, component

    def recount(self, table):
        with self.conn:
            data = self.cursor.execute(f'select ref_des, priority from {table}').fetchall()
            if data != []:
                if data[0][1] == 2:
                    self.cursor.execute(f'update {table} set priority = 1 where ref_des = "{data[0][0]}"')
                    data = self.cursor.execute(f'select ref_des, priority from {table}').fetchall()
                for count, element in enumerate(data):
                    if count == 0:
                        continue
                    prev_element = data[count - 1]
                    if element[1] - prev_element[1] > 1:
                        self.cursor.execute(
                            f'update {table} set priority = {prev_element[1] + 1} where ref_des = "{element[0]}"')
                        for index in range(count + 1, len(data)):
                            self.cursor.execute(
                                f'update {table} set priority = {data[index][1] - 1} where ref_des = "{data[index][0]}"'
                            )

    def move_up(self):
        table = self.components
        row = table.currentIndex().row()
        if row == -1:
            return
        model = table.model()
        ref_index = model.index(row, 0)
        ref_des = model.data(ref_index)
        count_index = model.index(row, 6)
        count = model.data(count_index)
        if count == 1:
            return
        project = self.comboBox.currentText()
        db_table = f'{project}_components'
        with self.conn:
            self.cursor.execute(f'update "{db_table}" set priority = {count} where priority = {count - 1}')
            self.cursor.execute(f'update "{db_table}" set priority = {count - 1} where ref_des = "{ref_des}"')
        self.components_filling()
        current_index = model.index(row - 1, 6)
        table.setCurrentIndex(current_index)

    def move_down(self):
        table = self.components
        row = table.currentIndex().row()
        if row == -1:
            return
        model = table.model()
        count_index = model.index(row, 6)
        current_count = model.data(count_index)
        count = self.increment() - 1
        if count < 2 or row == -1 or count == current_count:
            return
        ref_index = model.index(row, 0)
        ref_des = model.data(ref_index)
        project = self.comboBox.currentText()
        db_table = f'{project}_components'
        with self.conn:
            self.cursor.execute(
                f'update "{db_table}" set priority = {current_count} where priority = {current_count + 1}')
            self.cursor.execute(f'update "{db_table}" set priority = {current_count + 1} where ref_des = "{ref_des}"')
        self.components_filling()
        current_index = model.index(row + 1, 6)
        table.setCurrentIndex(current_index)

    def change_ui_set_enable(self):
        index = self.tabWidget_2.currentIndex()
        disabled = self.change_ui_disabled_fields
        enabled = self.change_ui_enabled_fields[index]
        if self.change_components.radioButton.isChecked():
            self.change_components.spinBox_3.setEnabled(False)
            self.change_components.spinBox_4.setEnabled(False)
            self.set_form_fields(disabled, enabled)
        else:
            self.form_disable(self.change_ui_forms)
            if self.change_components.radioButton_2.isChecked():
                self.change_components.spinBox_3.setEnabled(True)
                self.change_components.spinBox_4.setEnabled(False)
            else:
                self.change_components.spinBox_3.setEnabled(False)
                self.change_components.spinBox_4.setEnabled(True)

    def set_components_values(self):
        print('Set')
        # project = self.comboBox.currentText()
        # table = f'{project}_components'
        # index = self.change_elements.ref_box.currentIndex()
        # ref_des = self.change_elements.ref_box.currentText()
        # index = self.change_elements.comboBox.currentIndex()
        # values = self.checking_fields[index]
        # with self.conn:
        #     component_id = self.cursor.execute(
        #         f'select element_id from "{table}" where ref_des = "{ref_des}"').fetchone()[0]
        #     ids = self.cursor.execute('select id from components').fetchall()
        #     for i in ids:
        #         if i[0] == component_id:
        #             component = self.cursor.execute(
        #                 f'select {values} from components where id = "{component_id}"').fetchall()[0]
        #             self.change_elements.comboBox_2.setCurrentText(str(f'{component}'))

    def form_disable(self, forms):
        for i in forms:
            i.setEnabled(False)

    def del_element(self):
        project = self.comboBox.currentText()
        table_components = f'{project}_components'
        table = self.components
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите элемент')
            return
        model = table.model()
        ref_index = model.index(row, 0)
        ref = model.data(ref_index)
        with self.conn:
            self.cursor.execute(f'delete from "{table_components}" where ref_des = "{ref}"')

        self.recount(table_components)
        self.components_filling()
        self.elements_list(self.add_elements)
        self.elements_list(self.change_elements)

    def del_element_qwestion(self):
        table = self.components
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите элемент!')
            return
        qwest = QMessageBox()
        qwest.setWindowTitle("Удалить элемент")
        qwest.setText("Вы уверны, что хотите удалить элемент?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.delete_element_action)
        qwest.exec_()

    def delete_element_action(self, btn):
        if btn.text() in ['OK']:
            self.del_element()

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.statistic_request)
        dialog.exec_()

    def statistic_request(self, printer):
        print_tables = (self.components, self.statistic, self.statistic_2)
        project_name = self.comboBox.currentText()
        q = self.spinBox_2.value()
        titles = (f'Мотажная таблица проекта {project_name}',
                  f'Статистика проекта {project_name}',
                  f'Наличие компонентов для проекта {project_name}, количество комплектов: {q}')
        headers_width = ((16, 19, 15, 10, 10, 20, 10), (30, 15, 15, 10, 10, 20), (18, 13, 17, 10, 10, 10, 11, 11))
        index = self.tabWidget_3.currentIndex()
        table = print_tables[index]
        model = table.model()
        title = titles[index]
        rowcount = model.rowCount()
        columncount = model.columnCount()
        table_body = ''
        table_body += '<tr>'
        for h in range(columncount):
            width = headers_width[index][h]
            table_body += f'<td align="center" width="{width}%"> {model.headerData(h, Qt.Orientation.Horizontal)}</td>'
        table_body += '</tr>'
        for r in range(rowcount):
            table_body += '<tr>'
            for c in range(columncount):
                item_index = model.index(r, c)
                item = model.data(item_index)
                table_body += f'<td>{item}</td>'
            table_body += '</tr>'
        page = f'<!DOCTYPE html><html lang="ru">' \
               f'<head>' \
               f'<meta charset="UTF-8">' \
               f'</head>' \
               f'<body>' \
               f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
               f'<tr>' \
               f'<td colspan="{columncount}" align="center">{title}</td>' \
               f'</tr>' \
               f'{table_body}' \
               f'</table>' \
               f'</body>' \
               f'</html>'
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def add_project(self):
        project_name = str(self.projects.lineEdit.text())

        with self.conn:
            if project_name in (None, ''):
                self.show_error('Введите имя проекта!')
                return
            check = self.cursor.execute(f'select * from projects where project_name="{project_name}"').fetchone()

            if check is None:
                self.cursor.execute(f'INSERT INTO projects (project_name) values("{project_name}")')
                self.cursor.execute(f""
                                    f"CREATE TABLE '{project_name}_components' "
                                    f"(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                                    f"ref_des VARCHAR, priority INTEGER, element_id integer)")
            else:
                self.show_error('Такой проект уже имеется в базе!')
                return
        self.projects_filling()
        self.comboBox.addItem(project_name)
        self.projects.lineEdit.clear()

    def del_project_qwestion(self):
        table = self.projects.tableView
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите проект!')
            return
        qwest = QMessageBox()
        qwest.setWindowTitle("Удалить проект")
        qwest.setText("Вы уверны, что хотите удалить проект?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.project_action)
        qwest.exec_()

    def project_action(self, btn):
        if btn.text() in ['OK', '&OK']:
            self.del_project()

    def del_project(self):
        table = self.projects.tableView
        row = table.currentIndex().row()
        model = self.projects.tableView.model()
        id_index = model.index(row, 0)
        project_id = model.data(id_index)
        item_index = model.index(row, 1)
        item = model.data(item_index)
        for i in range(self.comboBox.count()):
            if self.comboBox.itemText(i) == item:
                self.comboBox.removeItem(i)
        with self.conn:
            self.cursor.execute(f'DELETE from projects WHERE id = "{project_id}"')
            self.cursor.execute(f'DROP TABLE IF EXISTS "{item}_components";')
        self.projects_filling()

    def add_case(self):
        group = self.cases.comboBox.currentText()
        case_name = self.cases.lineEdit.text()
        if case_name == '':
            self.show_error('Введите название корпуса!')
            return
        with self.conn:
            check = self.cursor.execute(f'select * from cases where type = "{group}" and casing = "{case_name}"')
            if check.fetchone() is None:
                self.cursor.execute(f'insert into cases (type, casing) values ("{group}", "{case_name}")')
                self.cases_filling()
            else:
                self.show_error('Такой корпус уже имеется в этой группе!')
        self.cases.lineEdit.clear()

    def del_case_qwestion(self):
        table = self.cases.tableView
        row = table.currentIndex().row()
        if row == -1:
            self.show_error('Выберите корпус!')
            return
        qwest = QMessageBox()
        qwest.setWindowTitle("Удалить корпус")
        qwest.setText("Вы уверны, что хотите удалить корпус?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.del_case_action)
        qwest.exec_()

    def del_case_action(self, btn):
        if btn.text() in ['OK']:
            self.del_case()

    def del_case(self):
        table = self.cases.tableView
        row = table.currentIndex().row()
        model = table.model()
        id_index = model.index(row, 0)
        case_id = model.data(id_index)
        with self.conn:
            self.cursor.execute(f'delete from cases where id = "{case_id}"')
        self.cases_filling()

    def unload_qwestion(self):
        qwest = QMessageBox()
        qwest.setWindowTitle("Выгрузка компонентов")
        qwest.setText("Выгрузить компоненты?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.unload_action)
        qwest.exec_()

    def unload_action(self, btn):
        if btn.text() in ['OK', '&OK']:
            self.unload()

    def unload(self):
        k = self.spinBox.value()
        db_table = f'{self.comboBox.currentText()}_components'
        with self.conn:
            elements = self.cursor.execute(f'select element_id from "{db_table}"').fetchall()
            for element_id in elements:
                quantity = self.cursor.execute(f'select quantity from components where id = {element_id[0]}').fetchone()
                sum = quantity[0] - k
                override = 0 if sum < 0 else sum
                self.cursor.execute(f'update components set quantity = {override} where id = {element_id[0]}')
            self.report('Выгружено', len(elements))
        self.filling()

    def report(self, message, quantity):
        report_ = QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        report_.setWindowIcon(icon)
        report_.setWindowTitle("Выгрузка компонентов")
        report_.setText(f"{message} компонентов: {quantity}")
        report_.setIcon(QMessageBox.Information)
        report_.setStandardButtons(QMessageBox.Ok)
        report_.exec_()

    def closeEvent(self, event):
        index_0 = str(self.tabWidget.currentIndex())
        index_1 = str(self.tabWidget_2.currentIndex())
        index_2 = str(self.tabWidget_3.currentIndex())
        combo_index = str(self.comboBox.currentIndex())
        toolbar = 'ON' if self.actionToolBar.isChecked() else 'OFF'
        self.config.set('INDEX', 'index_tab_0', index_0)
        self.config.set('INDEX', 'index_tab_1', index_1)
        self.config.set('INDEX', 'index_tab_2', index_2)
        self.config.set('INDEX', 'combo_index', combo_index)
        self.config.set('TOOLBAR', 'status', toolbar)
        with open('settings.ini', 'w') as f:
            self.config.write(f)

    @staticmethod
    def show_about(self):
        report_ = QMessageBox()
        report_.setWindowTitle("О программе")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        report_.setWindowIcon(icon)
        report_.setText('Программа организации хранения и использования электронных компонентов "База деталей 2.1"')
        report_.setIcon(QMessageBox.Information)
        report_.setStandardButtons(QMessageBox.Ok)
        report_.exec_()

    @staticmethod
    def show_help(self):
        os.system('hh.exe Base.chm')


class AddComponent(QDialog, Ui_Add_component):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ChangeComponent(QDialog, Ui_Change_component):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Projects(QDialog, Ui_Projects):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class AddElements(QDialog, Ui_Add_Element):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ChangeElements(QDialog, Ui_Change_Element):
    def __init__(self):
        super(ChangeElements, self).__init__()
        self.setupUi(self)


class Cases(QDialog, Ui_Cases):
    def __init__(self):
        super(Cases, self).__init__()
        self.setupUi(self)


class TableModel(QAbstractTableModel):

    def __init__(self, headers, data_in, parent=None):

        super().__init__(parent)
        self.headers = headers
        self.data_in = data_in
        self.insertRows(len(self.data_in), 1)
        self.items = []

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]

    def data(self, index, role):

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            value = self.data_in[row][col]
            return value

    def columnCount(self, parent):

        return len(self.headers)

    def rowCount(self, parent):

        return len(self.data_in)

    def insertRows(self, position, rows, parent=QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()
        return True



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
