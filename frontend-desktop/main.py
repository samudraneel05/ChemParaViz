import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QTabWidget, QFrame, QScrollArea,
    QGridLayout, QStackedWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


class APIClient:
    """Client for communicating with Django backend"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = f"Token {token}"
    
    def login(self, username, password):
        url = f"{self.base_url}/auth/login/"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        return response.json()
    
    def register(self, username, password, email=""):
        url = f"{self.base_url}/auth/register/"
        data = {"username": username, "password": password, "email": email}
        response = requests.post(url, json=data)
        return response.json()
    
    def upload_dataset(self, file_path):
        url = f"{self.base_url}/upload/"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.post(url, files=files, headers=headers)
        return response.json()
    
    def get_datasets(self):
        url = f"{self.base_url}/datasets-list/"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_dataset_detail(self, dataset_id):
        url = f"{self.base_url}/dataset/{dataset_id}/"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def delete_dataset(self, dataset_id):
        url = f"{self.base_url}/dataset/{dataset_id}/delete/"
        response = requests.delete(url, headers=self.headers)
        return response
    
    def download_report(self, dataset_id):
        url = f"{self.base_url}/dataset/{dataset_id}/report/"
        response = requests.get(url, headers=self.headers)
        return response.content


class LoginWindow(QWidget):
    """Login/Register window"""
    
    login_success = pyqtSignal(str, dict)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ChemParaViz - Login")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QWidget {
                background: #fafafa;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            QLineEdit {
                padding: 10px 14px;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                background: white;
                font-size: 13px;
                color: #171717;
            }
            QLineEdit:focus {
                border-color: #0a0a0a;
                outline: none;
            }
            QPushButton {
                padding: 10px 16px;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                background: #0a0a0a;
                color: white;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #262626;
            }
            QLabel {
                color: #171717;
                font-size: 13px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left side - branding
        left_widget = QWidget()
        left_widget.setStyleSheet("background: #ffffff; border-right: 1px solid #e5e5e5;")
        left_widget.setMinimumWidth(450)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(60, 60, 60, 60)
        
        title = QLabel("ChemParaViz")
        title.setFont(QFont("Inter", 32, QFont.Bold))
        title.setStyleSheet("color: #171717; font-weight: 600; letter-spacing: -0.02em;")
        title.setAlignment(Qt.AlignLeft)
        left_layout.addWidget(title)
        
        subtitle = QLabel("Chemical Equipment\nParameter Visualizer")
        subtitle.setFont(QFont("Inter", 16))
        subtitle.setStyleSheet("color: #737373; line-height: 1.6;")
        subtitle.setAlignment(Qt.AlignLeft)
        left_layout.addWidget(subtitle)
        left_layout.addStretch()
        
        # Right side - form
        right_widget = QWidget()
        right_widget.setStyleSheet("background: #fafafa;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(60, 60, 60, 60)
        
        form_widget = QWidget()
        form_widget.setStyleSheet("background: transparent;")
        form_widget.setMaximumWidth(350)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        
        form_title = QLabel("Sign in")
        form_title.setFont(QFont("Inter", 24, QFont.Bold))
        form_title.setStyleSheet("color: #171717; font-weight: 600;")
        form_layout.addWidget(form_title)
        
        form_layout.addSpacing(10)
        
        # Username
        username_label = QLabel("USERNAME")
        username_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; letter-spacing: 0.05em;")
        form_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(40)
        form_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("PASSWORD")
        password_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; letter-spacing: 0.05em;")
        form_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        form_layout.addWidget(self.password_input)
        
        # Email (for registration)
        email_label = QLabel("EMAIL (OPTIONAL)")
        email_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; letter-spacing: 0.05em;")
        self.email_label = email_label
        form_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(40)
        form_layout.addWidget(self.email_input)
        
        # Hide email initially
        self.email_label.hide()
        self.email_input.hide()
        
        form_layout.addSpacing(10)
        
        # Login button
        self.login_btn = QPushButton("Sign in")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: #0a0a0a;
                color: white;
                border: none;
                border-radius: 2px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #262626;
            }
        """)
        self.login_btn.clicked.connect(self.handle_auth)
        form_layout.addWidget(self.login_btn)
        
        # Toggle button
        self.toggle_btn = QPushButton("Don't have an account? Register")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #737373;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #171717;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        form_layout.addWidget(self.toggle_btn)
        
        right_layout.addWidget(form_widget)
        
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.setLayout(layout)
        
        self.is_register_mode = False
    
    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode:
            self.login_btn.setText("Register")
            self.login_btn.setStyleSheet("""
                QPushButton {
                    background: #0a0a0a;
                    color: white;
                    border: none;
                    border-radius: 2px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: #262626;
                }
            """)
            self.toggle_btn.setText("Already have an account? Sign in")
            self.email_label.show()
            self.email_input.show()
        else:
            self.login_btn.setText("Sign in")
            self.login_btn.setStyleSheet("""
                QPushButton {
                    background: #0a0a0a;
                    color: white;
                    border: none;
                    border-radius: 2px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: #262626;
                }
            """)
            self.toggle_btn.setText("Don't have an account? Register")
            self.email_label.hide()
            self.email_input.hide()
    
    def handle_auth(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        try:
            if self.is_register_mode:
                email = self.email_input.text()
                result = self.api_client.register(username, password, email)
            else:
                result = self.api_client.login(username, password)
            
            if 'token' in result:
                self.api_client.set_token(result['token'])
                self.login_success.emit(result['token'], result['user'])
                self.close()
            else:
                QMessageBox.warning(self, "Error", result.get('error', 'Authentication failed'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), facecolor='#ffffff')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Set consistent font for matplotlib
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
        plt.rcParams['font.size'] = 11
    
    def plot_pie_chart(self, data, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#ffffff')
        labels = list(data.keys())
        values = list(data.values())
        colors = ['#0284c7', '#0891b2', '#14b8a6', '#10b981', '#84cc16', '#eab308']
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                           colors=colors[:len(labels)],
                                           wedgeprops={'edgecolor': 'white', 'linewidth': 1},
                                           textprops={'fontsize': 10, 'color': '#171717', 'family': 'sans-serif'})
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', color='#171717', pad=20)
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.canvas.draw()
    
    def plot_bar_chart(self, labels, values, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#ffffff')
        colors = ['#0284c7', '#14b8a6', '#84cc16']
        bars = ax.bar(labels, values, color=colors[:len(labels)], 
                     edgecolor='#e5e5e5', linewidth=1)
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', color='#171717', pad=20)
        ax.set_ylabel('Value', fontsize=10, color='#737373')
        ax.tick_params(colors='#737373', labelsize=10)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily('sans-serif')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e5e5')
        ax.spines['bottom'].set_color('#e5e5e5')
        ax.grid(axis='y', alpha=0.2, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        self.figure.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        self.canvas.draw()


class DashboardWindow(QMainWindow):
    """Main dashboard window"""
    
    def __init__(self, api_client, user):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.datasets = []
        self.current_dataset = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        self.setWindowTitle("ChemParaViz - Dashboard")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("""
            QMainWindow {
                background: #fafafa;
            }
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                background: #ffffff;
                color: #171717;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #fafafa;
            }
            QLabel {
                color: #171717;
            }
            QTableWidget {
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                gridline-color: #e5e5e5;
            }
            QTableWidget::item {
                padding: 12px 16px;
                color: #737373;
            }
            QHeaderView::section {
                background: #fafafa;
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid #e5e5e5;
                font-weight: 600;
                font-size: 11px;
                color: #171717;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet("""
            background: #ffffff;
            border-bottom: 1px solid #e5e5e5;
        """)
        header.setFixedHeight(64)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 0, 32, 0)
        
        title = QLabel("ChemParaViz Dashboard")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setStyleSheet("color: #171717; font-weight: 600; letter-spacing: -0.02em;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        user_label = QLabel(f"Welcome, {self.user['username']}!")
        user_label.setStyleSheet("color: #737373; font-size: 14px;")
        header_layout.addWidget(user_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 14px;
                background: transparent;
                color: #171717;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #fafafa;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        
        main_layout.addWidget(header)
        
        # Content area
        content = QWidget()
        content.setStyleSheet("background: #fafafa;")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background: #ffffff; border-right: 1px solid #e5e5e5;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(32)
        
        upload_label = QLabel("UPLOAD DATASET")
        upload_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; letter-spacing: 0.05em;")
        sidebar_layout.addWidget(upload_label)
        
        upload_btn = QPushButton("Choose CSV File")
        upload_btn.setStyleSheet("""
            QPushButton {
                background: #0a0a0a;
                color: white;
                padding: 10px 14px;
                border: none;
                border-radius: 2px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #262626;
            }
        """)
        upload_btn.clicked.connect(self.upload_file)
        sidebar_layout.addWidget(upload_btn)
        
        datasets_label = QLabel("MY DATASETS")
        datasets_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; letter-spacing: 0.05em;")
        sidebar_layout.addWidget(datasets_label)
        
        # Datasets list
        self.datasets_widget = QWidget()
        self.datasets_widget.setStyleSheet("background: transparent;")
        self.datasets_layout = QVBoxLayout(self.datasets_widget)
        self.datasets_layout.setAlignment(Qt.AlignTop)
        self.datasets_layout.setSpacing(6)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.datasets_widget)
        scroll.setStyleSheet("border: none; background: transparent;")
        sidebar_layout.addWidget(scroll)
        
        content_layout.addWidget(sidebar)
        
        # Main content
        self.main_content = QWidget()
        self.main_content.setStyleSheet("background: #fafafa;")
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(32, 32, 32, 32)
        self.main_content_layout.setSpacing(32)
        
        self.empty_state = QLabel("No Dataset Selected\n\nUpload a CSV file to get started")
        self.empty_state.setAlignment(Qt.AlignCenter)
        self.empty_state.setFont(QFont("Arial", 18))
        self.empty_state.setStyleSheet("color: #a3a3a3;")
        self.main_content_layout.addWidget(self.empty_state)
        
        self.data_view = QWidget()
        self.data_view.setStyleSheet("background: transparent;")
        self.data_view_layout = QVBoxLayout(self.data_view)
        self.data_view_layout.setContentsMargins(0, 0, 0, 0)
        self.data_view_layout.setSpacing(32)
        self.data_view.hide()
        self.main_content_layout.addWidget(self.data_view)
        
        content_layout.addWidget(self.main_content)
        
        main_layout.addWidget(content)
    
    def load_datasets(self):
        try:
            self.datasets = self.api_client.get_datasets()
            self.update_datasets_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load datasets: {str(e)}")
    
    def update_datasets_list(self):
        # Clear existing items
        while self.datasets_layout.count():
            child = self.datasets_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add dataset items
        for dataset in self.datasets:
            item = QPushButton(f"{dataset['filename']}\n{dataset['uploaded_at'][:10]}")
            item.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 2px;
                    padding: 12px;
                    text-align: left;
                    font-size: 13px;
                    color: #171717;
                }
                QPushButton:hover {
                    background: #fafafa;
                    border-color: #e5e5e5;
                }
            """)
            item.clicked.connect(lambda checked, d=dataset: self.load_dataset_detail(d['id']))
            self.datasets_layout.addWidget(item)
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                result = self.api_client.upload_dataset(file_path)
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
                self.load_datasets()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload: {str(e)}")
    
    def load_dataset_detail(self, dataset_id):
        try:
            detail = self.api_client.get_dataset_detail(dataset_id)
            self.current_dataset = dataset_id
            self.display_dataset_detail(detail)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {str(e)}")
    
    def display_dataset_detail(self, detail):
        self.empty_state.hide()
        self.data_view.show()
        
        # Clear existing content
        while self.data_view_layout.count():
            child = self.data_view_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Header with actions
        header_widget = QWidget()
        header_widget.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        header_title = QLabel("Dataset Analysis")
        header_title.setFont(QFont("Arial", 20, QFont.Bold))
        header_title.setStyleSheet("color: #171717;")
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        report_btn = QPushButton("Download Report")
        report_btn.clicked.connect(self.download_report)
        header_layout.addWidget(report_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                border: 1px solid #dc2626;
                color: #dc2626;
            }
            QPushButton:hover {
                background: #fef2f2;
            }
        """)
        delete_btn.clicked.connect(self.delete_dataset)
        header_layout.addWidget(delete_btn)
        
        self.data_view_layout.addWidget(header_widget)
        
        # Stats grid
        stats_widget = QWidget()
        stats_widget.setStyleSheet("background: transparent;")
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(16)
        stats_layout.setContentsMargins(0, 0, 0, 20)
        
        stats_data = [
            ("TOTAL EQUIPMENT", str(detail['total_count'])),
            ("AVG FLOWRATE", f"{detail['averages']['flowrate']:.2f}"),
            ("AVG PRESSURE", f"{detail['averages']['pressure']:.2f}"),
            ("AVG TEMPERATURE", f"{detail['averages']['temperature']:.2f}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            stat_card = QWidget()
            stat_card.setStyleSheet("""
                QWidget {
                    background: #ffffff;
                    border: 1px solid #e5e5e5;
                    border-radius: 2px;
                }
            """)
            stat_card.setFixedHeight(100)
            stat_layout_inner = QVBoxLayout(stat_card)
            stat_layout_inner.setContentsMargins(20, 20, 20, 20)
            
            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: #a3a3a3; font-size: 11px; font-weight: 600; background: transparent; border: none;")
            stat_layout_inner.addWidget(stat_label)
            
            stat_value = QLabel(value)
            stat_value.setFont(QFont("Arial", 28, QFont.Bold))
            stat_value.setStyleSheet("color: #171717; background: transparent; border: none;")
            stat_layout_inner.addWidget(stat_value)
            
            stats_layout.addWidget(stat_card, 0, i)
        
        self.data_view_layout.addWidget(stats_widget)
        
        # Charts row
        charts_widget = QWidget()
        charts_widget.setStyleSheet("background: transparent;")
        charts_layout = QHBoxLayout(charts_widget)
        charts_layout.setSpacing(16)
        charts_layout.setContentsMargins(0, 0, 0, 20)
        
        # Pie chart
        pie_container = self.create_chart_card("Equipment Type Distribution")
        pie_widget = ChartWidget()
        pie_widget.plot_pie_chart(detail['equipment_type_distribution'], "")
        pie_container.layout().addWidget(pie_widget)
        charts_layout.addWidget(pie_container)
        
        # Bar chart
        bar_container = self.create_chart_card("Average Parameters")
        bar_widget = ChartWidget()
        bar_widget.plot_bar_chart(
            ['Flowrate', 'Pressure', 'Temperature'],
            [detail['averages']['flowrate'], 
             detail['averages']['pressure'],
             detail['averages']['temperature']],
            ""
        )
        bar_container.layout().addWidget(bar_widget)
        charts_layout.addWidget(bar_container)
        
        self.data_view_layout.addWidget(charts_widget)
        
        # Table
        table_container = self.create_chart_card("Equipment Details")
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        table.setRowCount(len(detail['equipment_details']))
        
        for i, eq in enumerate(detail['equipment_details']):
            table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            table.setItem(i, 2, QTableWidgetItem(str(eq['flowrate'])))
            table.setItem(i, 3, QTableWidgetItem(str(eq['pressure'])))
            table.setItem(i, 4, QTableWidgetItem(str(eq['temperature'])))
        
        # Stretch columns to fill space
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        header.setSectionResizeMode(3, header.Stretch)
        header.setSectionResizeMode(4, header.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setMinimumHeight(300)
        table_container.layout().addWidget(table)
        self.data_view_layout.addWidget(table_container)
    
    def create_chart_card(self, title):
        """Helper to create consistent card containers"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #171717; background: transparent; border: none;")
        layout.addWidget(title_label)
        
        return container
    
    def download_report(self):
        if not self.current_dataset:
            return
        
        try:
            pdf_content = self.api_client.download_report(self.current_dataset)
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Report", f"report_{self.current_dataset}.pdf", "PDF Files (*.pdf)"
            )
            
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                QMessageBox.information(self, "Success", "Report downloaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download report: {str(e)}")
    
    def delete_dataset(self):
        if not self.current_dataset:
            return
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this dataset?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(self.current_dataset)
                QMessageBox.information(self, "Success", "Dataset deleted successfully!")
                self.current_dataset = None
                self.empty_state.show()
                self.data_view.hide()
                self.load_datasets()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete dataset: {str(e)}")
    
    def logout(self):
        self.close()
        login_window = LoginWindow(self.api_client)
        login_window.login_success.connect(lambda token, user: show_dashboard(self.api_client, user))
        login_window.show()
        self.login_window = login_window


def show_dashboard(api_client, user):
    dashboard = DashboardWindow(api_client, user)
    dashboard.show()
    return dashboard


def main():
    app = QApplication(sys.argv)
    
    api_client = APIClient()
    login_window = LoginWindow(api_client)
    login_window.login_success.connect(lambda token, user: show_dashboard(api_client, user))
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
