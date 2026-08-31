from reportlab.pdfgen import canvas
from pathlib import Path

output = Path("input/document.pdf")

output.parent.mkdir(exist_ok=True)

pdf = canvas.Canvas(str(output))

pdf.drawString(100, 750, "Day 10 Async PDF Processing")
pdf.drawString(100, 720, "This is a test PDF for my Hybrid RAG project.")
pdf.drawString(100, 690, "The worker will extract this text.")
pdf.drawString(100, 660, "PDF processing is working successfully.")

pdf.save()

print("PDF created successfully!")
print(f"Saved to: {output}")