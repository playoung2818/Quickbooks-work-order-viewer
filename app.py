import os
import json
import logging
from flask import render_template, request, send_file, abort, jsonify
from models import db, PDFFileLog, WordFileLog
from create_app import create_app
# from file_parser import merge_inventory_status

app = create_app()  

@app.route('/api/word-files', methods=['GET'])
def get_word_files():
    try:
        word_files = WordFileLog.query.all()
        word_files_data = [
            {
                "file_name": w.file_name,
                "order_id": w.order_id,
                "status": "Picked" if w.product_details else "No",
                "file_path": w.file_path
            }
            for w in word_files
        ]
        return jsonify({"word_files": word_files_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/view_file/<path:file_path>')
def view_file(file_path):
    if not os.path.exists(file_path):
        abort(404, description="File not found")
    return send_file(file_path, as_attachment=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '').strip().lower()
    pdf_results = PDFFileLog.query.filter(PDFFileLog.file_name.ilike(f"%{search_query}%")).all()
    word_results = WordFileLog.query.filter(WordFileLog.file_name.ilike(f"%{search_query}%")).all()

    word_data = []
    for word in word_results:
        try:
            product_details = word.product_details if isinstance(word.product_details, list) else json.loads(word.product_details)
            for entry in product_details:
                word_data.append({
                    "file_name": word.file_name,
                    "file_path": word.file_path,
                    "product_number": entry.get("product_number", "N/A"),
                    "qty": entry.get("qty", "N/A"),
                    "sn": entry.get("sn", "N/A"),
                    "notes": entry.get("notes", "N/A")
                })
        except Exception as e:
            logging.error(f"[ERROR] Failed parsing product details for {word.file_name}: {e}")


    return render_template(
        'index.html',
        pdf_results=pdf_results,
        word_data=word_data,
        search_query=search_query,
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)



