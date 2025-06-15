import json

def json_to_html(json_file: str, html_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        channels = json.load(f)

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
        <th onclick="sortTable(4)">Средний просмотр</th>
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

    // Снять старую подсветку
    var ths = table.tHead.rows[0].cells;
    for (var i = 0; i < ths.length; i++) {
      ths[i].classList.remove("sorted-asc", "sorted-desc");
    }

    // Добавить новую стрелку
    ths[n].classList.add(asc ? "sorted-asc" : "sorted-desc");

    // Подсветить колонку
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

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML-отчёт с визуальной сортировкой сохранён в {html_file}")

if __name__ == "__main__":

    json_to_html("TgChannels.json", "channels_report.html")
