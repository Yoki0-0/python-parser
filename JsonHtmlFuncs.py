from pathlib import Path
import json
from typing import List
from ChannelDataclass import Channel
def json_to_html(json_file: str, html_file: str):
    with open("jsons/" + json_file, "r", encoding="utf-8") as f:
        channels = json.load(f)


    output_dir = Path("webs")
    output_dir.mkdir(parents=True, exist_ok=True)

    full_path = output_dir / html_file

    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Отчёт по каналам</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background-color: #f0f0f0; cursor: pointer; position: relative; }
    th.sorted-asc::after { content: " ↑"; position: absolute; right: 8px; }
    th.sorted-desc::after { content: " ↓"; position: absolute; right: 8px; }
    tbody td.active-col { background-color: #f9f9f9; }
    h1 { text-align: center; }
  </style>
</head>
<body>
  <h1>Отчёт по каналам</h1>
  <table id="channelsTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Название</th>
        <th onclick="sortTable(1)">Ссылка</th>
        <th onclick="sortTable(2)">Категория</th>
        <th onclick="sortTable(3)">Подписчики</th>
        <th onclick="sortTable(4)">Средний охват</th>
        <th onclick="sortTable(5)">ERR (%)</th>
        <th onclick="sortTable(6)">Миграция 7д</th>
        <th onclick="sortTable(7)">Миграция 30д</th>
        <th onclick="sortTable(8)">Возраст</th>
      </tr>
    </thead>
    <tbody>
"""

    for ch in channels:
        html += f"""
      <tr>
        <td>{ch.get("name", "")}</td>
        <td><a href="{ch.get("link", "")}">{ch.get("link", "")}</a></td>
        <td>{ch.get("category", "")}</td>
        <td>{ch.get("subs", "")}</td>
        <td>{ch.get("avg_views_post", "")}</td>
        <td>{ch.get("err", "")}</td>
        <td>{ch.get("migr_sub7d", "")}</td>
        <td>{ch.get("migr_sub30d", "")}</td>
        <td>{ch.get("lifetime", "")}</td>
      </tr>
"""

    html += """
    </tbody>
  </table>

  <script>
  function sortTable(n) {
    var table = document.getElementById("channelsTable");
    var rows = Array.from(table.rows).slice(1);
    var asc = table.getAttribute("data-sort-col") != n || table.getAttribute("data-sort-order") == "desc";

    rows.sort(function(rowA, rowB) {
      var a = rowA.cells[n].innerText.replace(/\\s+/g, '').replace(',', '.');
      var b = rowB.cells[n].innerText.replace(/\\s+/g, '').replace(',', '.');
      var numA = parseFloat(a);
      var numB = parseFloat(b);
      if (!isNaN(numA) && !isNaN(numB)) {
        return asc ? numA - numB : numB - numA;
      } else {
        return asc ? a.localeCompare(b) : b.localeCompare(a);
      }
    });

    for (var row of rows) table.tBodies[0].appendChild(row);

    var ths = table.tHead.rows[0].cells;
    for (var i = 0; i < ths.length; i++) {
      ths[i].classList.remove("sorted-asc", "sorted-desc");
    }

    ths[n].classList.add(asc ? "sorted-asc" : "sorted-desc");

    for (var r of rows) {
      for (var i = 0; i < r.cells.length; i++) {
        r.cells[i].classList.toggle("active-col", i == n);
      }
    }

    table.setAttribute("data-sort-col", n);
    table.setAttribute("data-sort-order", asc ? "asc" : "desc");
  }
  </script>

</body>
</html>
"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML-отчёт с визуальной сортировкой сохранён в {full_path}")

def save_channels_to_json(channels: List[Channel], filename: str):
    output_dir = Path("jsons")
    output_dir.mkdir(parents=True, exist_ok=True)

    full_path = output_dir / (filename + ".json")

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)
def process_all_jsons():
    json_dir = Path("jsons")
    for json_file in json_dir.glob("*.json"):
        name = json_file.stem
        html_file = f"{name} Отчёт.html"
        print(f"🔹 Обработка {json_file.name} → {html_file}")
        json_to_html(json_file.name, html_file)

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