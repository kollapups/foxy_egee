# import json
# import os
# from weasyprint import HTML, CSS
# from django.conf import settings
# settings.configure(MEDIA_ROOT="/path/to/media")

# def render_latex_to_svg(latex):
#     """Конвертирует LaTeX в SVG с помощью node-mathjax."""
#     # Создаем временный файл с LaTeX
#     temp_file = os.path.join(settings.MEDIA_ROOT, "temp_latex.json")
#     with open(temp_file, "w") as f:
#         json.dump({"math": latex, "format": "TeX", "svg": True}, f)

#     # Вызываем node-mathjax
#     result = subprocess.run(
#         ["node", "render_latex.js", temp_file],
#         capture_output=True,
#         text=True,
#     )

#     if result.returncode == 0:
#         svg_output = result.stdout
#         return svg_output
#     else:
#         raise Exception(f"MathJax error: {result.stderr}")

# # Пример Node.js скрипта (render_latex.js)
# with open("render_latex.js", "w") as f:
#     f.write("""
# const fs = require('fs');
# const mathjax = require('mathjax-node');

# mathjax.start();

# const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
# mathjax.typeset({
#     math: input.math,
#     format: input.format,
#     svg: input.svg
# }, function(data) {
#     if (data.errors) {
#         console.error(data.errors);
#         process.exit(1);
#     }
#     console.log(data.svg);
# });
# """)

# def process_tasks():
#     with open("tasks_data.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     tasks = [item for item in data if item["model"] == "tasks.task"]
#     for task in tasks:
#         text = task["fields"]["text"]
#         solution_text = task["fields"]["solution_text"]
#         import re

#         def replace_latex(match):
#             latex = match.group(1) or match.group(2)
#             return render_latex_to_svg(latex)

#         task["fields"]["text"] = re.sub(r"\$\$(.*?)\$\$|\$(.*?)\$", replace_latex, text)
#         if solution_text:
#             task["fields"]["solution_text"] = re.sub(r"\$\$(.*?)\$\$|\$(.*?)\$", replace_latex, solution_text)

#         # Генерация PDF
#         html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head><meta charset="UTF-8"><title>Task {task['fields']['unique_id']}</title></head>
#         <body>
#             <h3>Задание {task['fields']['exam_line']}</h3>
#             <div>{task['fields']['text']}</div>
#             <div>{task['fields']['solution_text']}</div>
#             <p><strong>Ответ:</strong> {task['fields']['answer']}</p>
#         </body>
#         </html>
#         """
#         pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string="@page { size: A4; margin: 1cm; }")])
#         with open(f"task_{task['fields']['unique_id']}.pdf", "wb") as f:
#             f.write(pdf)

# if __name__ == "__main__":
#     process_tasks()
