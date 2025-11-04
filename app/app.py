from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

# Konfigurasi
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kamus-modern-2025-secret-key'
    DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en"

app.config.from_object(Config)

class ModernDictionary:
    def __init__(self):
        self.menu_items = [
            {"name": "Beranda", "icon": "🏠", "id": "home"},
            {"name": "Kamus", "icon": "📚", "id": "dictionary"},
            {"name": "Favorit", "icon": "⭐", "id": "favorites"},
            {"name": "Riwayat", "icon": "🕒", "id": "history"},
            {"name": "Kategori", "icon": "📁", "id": "categories"},
            {"name": "Belajar", "icon": "🎓", "id": "learn"},
            {"name": "Quiz", "icon": "❓", "id": "quiz"},
            {"name": "Pengaturan", "icon": "⚙️", "id": "settings"},
            {"name": "Bantuan", "icon": "❔", "id": "help"},
            {"name": "Tentang", "icon": "ℹ️", "id": "about"}
        ]
        
        self.external_links = [
            {"name": "Kamus Online", "url": "https://kbbi.kemdikbud.go.id", "icon": "🌐"},
            {"name": "Translate", "url": "https://translate.google.com", "icon": "🔤"},
            {"name": "Sinonim", "url": "https://www.thesaurus.com", "icon": "🔄"},
            {"name": "Grammar", "url": "https://www.grammarly.com", "icon": "📝"},
            {"name": "Belajar Bahasa", "url": "https://www.duolingo.com", "icon": "🎯"},
            {"name": "AI Assistant", "url": "https://chat.openai.com", "icon": "🤖"},
            {"name": "E-Book", "url": "https://www.gutenberg.org", "icon": "📖"},
            {"name": "Podcast", "url": "https://www.spotify.com", "icon": "🎧"},
            {"name": "Forum", "url": "https://www.reddit.com/r/indonesia", "icon": "💬"},
            {"name": "Cloud Save", "url": "https://drive.google.com", "icon": "☁️"}
        ]
        
        self.search_history = []
        self.favorites = []

    def search_word(self, word):
        """Mencari arti kata menggunakan API"""
        try:
            response = requests.get(f"{app.config['DICTIONARY_API']}/{word.lower()}")
            if response.status_code == 200:
                data = response.json()
                self.search_history.append(word)
                # Simpan maksimal 50 riwayat
                if len(self.search_history) > 50:
                    self.search_history.pop(0)
                return data
            else:
                return {"error": "Kata tidak ditemukan dalam kamus"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Koneksi error: {str(e)}"}
        except Exception as e:
            return {"error": f"Terjadi kesalahan: {str(e)}"}

# Inisialisasi kamus
dictionary = ModernDictionary()

# ROUTES
@app.route('/')
def index():
    """Serve file index.html dari root folder"""
    return send_file('index.html')

@app.route('/search', methods=['POST'])
def search():
    word = request.json.get('word', '').strip()
    if not word:
        return jsonify({"error": "Kata tidak boleh kosong"})
    
    if len(word) > 50:
        return jsonify({"error": "Kata terlalu panjang"})
        
    result = dictionary.search_word(word)
    return jsonify(result)

@app.route('/favorites', methods=['GET', 'POST'])
def manage_favorites():
    if request.method == 'POST':
        word = request.json.get('word', '').strip()
        if word and word not in dictionary.favorites:
            dictionary.favorites.append(word)
        return jsonify({"success": True, "favorites": dictionary.favorites})
    else:
        return jsonify({"favorites": dictionary.favorites})

@app.route('/favorites/remove', methods=['POST'])
def remove_favorite():
    word = request.json.get('word', '').strip()
    if word in dictionary.favorites:
        dictionary.favorites.remove(word)
    return jsonify({"success": True, "favorites": dictionary.favorites})

@app.route('/history')
def get_history():
    return jsonify({"history": dictionary.search_history[-10:]})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Kamus Modern 2025 is running!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
