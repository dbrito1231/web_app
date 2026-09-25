from pathlib import Path

html = Path(r"C:\Users\dbadmin\Downloads\CCNA Lab Workbook\index.html").read_text(
    encoding="utf-8"
)
idx = html.find("<style>\n:root{")
if idx < 0:
    idx = html.find("<style>\r\n:root{")
end = html.find("</style>", idx)
css = html[idx + 7 : end]
out = Path(r"C:\Users\dbadmin\Desktop\GitServ\ccna\web_app\.cursor\ccna-tokens.css")
out.write_text(css, encoding="utf-8")
print("wrote", out, "chars", len(css))
