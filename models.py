from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PDFFileLog(db.Model):
    __tablename__ = 'pdf_file_log'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    extracted_data = db.Column(db.JSON, nullable=True)

class WordFileLog(db.Model):
    __tablename__ = 'word_file_log'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    product_details = db.Column(db.JSON, nullable=True)
    file_path = db.Column(db.String(255), nullable=False)
