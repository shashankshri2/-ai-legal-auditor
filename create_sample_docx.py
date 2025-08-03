from docx import Document

doc = Document()
doc.add_paragraph("This is a legal draft referring to ABC vs XYZ, [2015] 2 SCC 305 and DEF vs GHI, AIR 2020 SC 123.")
doc.save("data/draft.docx")

print("✅ Valid draft.docx created successfully.")
