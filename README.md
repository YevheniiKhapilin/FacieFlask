Класифікація ширини щелепи за допомогою Flask і MediaPipe
Цей проєкт дозволяє визначити тип щелепи (вузька, середня, широка) на основі завантаженої фотографії обличчя. Використовується модель MediaPipe FaceMesh, а також аналіз різних ключових точок на обличчі.

Технології
Python 3.8+

Flask

OpenCV

MediaPipe



1) Як запустити
Клонувати репозиторій:
git clone https://github.com/eughappy/FacieFlask.git
cd FacieFlask
Terminal:
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
python FlaskFacie.py
http://127.0.0.1:5000


2) Як це працює
Користувач завантажує зображення обличчя.
Модель MediaPipe знаходить ключові точки на обличчі.
Алгоритм обчислює відстані між точками щелепи, скронь, щік тощо.
Визначається коефіцієнт jaw/temple_ratio, що дозволяє класифікувати форму щелепи.
На результаті зображення малюються лінії між обраними точками.

3) Структура проєкту
│
├── FlaskFacie.py          # Головний Flask-сервер
├── analysis.py            # Логіка аналізу обличчя
├── templates/
│   └── index.html         # Інтерфейс завантаження фото
├── static/
│   ├── result.jpg         # Збережене зображення з візуалізацією
│   └── upload.jpg         # Завантажене зображення
├── requirements.txt       # Список залежностей
└── README.md              # Документація
