from main import json_to_html
from pathlib import Path

def process_all_jsons(json_dir="jsons", output_dir="webs"):
    json_path = Path(json_dir)
    html_path = Path(output_dir)
    html_path.mkdir(parents=True, exist_ok=True)

    json_files = json_path.glob("*.json")

    for json_file in json_files:
        name = json_file.stem  # имя файла без расширения
        html_file = f"{name} Отчёт.html"
        print(f"🔹 Обработка: {json_file} → {html_path / html_file}")
        json_to_html(str(json_file), html_file)

def generate_main_report(category_pairs: list[tuple[str, str]], output_filename="ОбщийОтчёт.html"):
    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Общий отчёт по категориям</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    nav { margin-bottom: 20px; }
    nav a { display: inline-block; margin: 5px; padding: 5px 10px; background: #f0f0f0; border-radius: 4px; text-decoration: none; color: #333; }
    nav a:hover { background: #ddd; }
    iframe { width: 100%; height: 80vh; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h1>Общий отчёт по категориям</h1>
  <nav>
"""

    for name, _ in category_pairs:
        file_name = f"webs/{name} Отчёт.html"
        html += f'<a href="#" onclick="loadReport(\'{file_name}\')">{name}</a>\n'

    html += """
  </nav>
  <iframe id="reportFrame" src=""></iframe>

  <script>
    function loadReport(file) {
      document.getElementById("reportFrame").src = file;
    }
  </script>
</body>
</html>
"""

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Главный отчёт создан: {output_filename}")
cat = [('Все категории', '/ratings/channels?sort=members'), ('Блоги', '/ratings/channels/blogs?sort=members'), ('Новости и СМИ', '/ratings/channels/news?sort=members'), ('Юмор и развлечения', '/ratings/channels/entertainment?sort=members'), ('Технологии', '/ratings/channels/tech?sort=members'), ('Экономика', '/ratings/channels/economics?sort=members'), ('Бизнес и стартапы', '/ratings/channels/business?sort=members'), ('Криптовалюты', '/ratings/channels/crypto?sort=members'), ('Путешествия', '/ratings/channels/travels?sort=members'), ('Маркетинг, PR, реклама', '/ratings/channels/marketing?sort=members'), ('Психология', '/ratings/channels/psychology?sort=members'), ('Дизайн', '/ratings/channels/design?sort=members'), ('Политика', '/ratings/channels/politics?sort=members'), ('Искусство', '/ratings/channels/art?sort=members'), ('Право', '/ratings/channels/law?sort=members'), ('Образование', '/ratings/channels/education?sort=members'), ('Книги', '/ratings/channels/books?sort=members'), ('Лингвистика', '/ratings/channels/language?sort=members'), ('Карьера', '/ratings/channels/career?sort=members'), ('Познавательное', '/ratings/channels/edutainment?sort=members'), ('Курсы и гайды', '/ratings/channels/courses?sort=members'), ('Спорт', '/ratings/channels/sport?sort=members'), ('Мода и красота', '/ratings/channels/beauty?sort=members'), ('Медицина', '/ratings/channels/medicine?sort=members'), ('Здоровье и Фитнес', '/ratings/channels/health?sort=members'), ('Картинки и фото', '/ratings/channels/pics?sort=members'), ('Софт и приложения', '/ratings/channels/apps?sort=members'), ('Видео и фильмы', '/ratings/channels/video?sort=members'), ('Музыка', '/ratings/channels/music?sort=members'), ('Игры', '/ratings/channels/games?sort=members'), ('Еда и кулинария', '/ratings/channels/food?sort=members'), ('Цитаты', '/ratings/channels/quotes?sort=members'), ('Рукоделие', '/ratings/channels/handmade?sort=members'), ('Семья и дети', '/ratings/channels/babies?sort=members'), ('Природа', '/ratings/channels/nature?sort=members'), ('Интерьер и строительство', '/ratings/channels/construction?sort=members'), ('Telegram', '/ratings/channels/telegram?sort=members'), ('Инстаграм', '/ratings/channels/instagram?sort=members'), ('Продажи', '/ratings/channels/sales?sort=members'), ('Транспорт', '/ratings/channels/transport?sort=members'), ('Религия', '/ratings/channels/religion?sort=members'), ('Эзотерика', '/ratings/channels/esoterics?sort=members'), ('Даркнет', '/ratings/channels/darknet?sort=members'), ('Букмекерство', '/ratings/channels/gambling?sort=members'), ('Шок-контент', '/ratings/channels/shock?sort=members'), ('Эротика', '/ratings/channels/erotica?sort=members'), ('Для взрослых', '/ratings/channels/adult?sort=members'), ('Другое', '/ratings/channels/other?sort=members')]
generate_main_report(cat)
process_all_jsons()
