from zipfile import ZipFile
import re
xml = ZipFile("thesis/full_thesis.docx").read("word/document.xml").decode("utf-8")
print("anchors", len(re.findall(r"w:anchor=", xml)))
print("bookmarks", len(re.findall(r"w:bookmarkStart", xml)))
print("ref_", len(re.findall(r"w:name=\"ref_", xml)))
print("fig_", len(re.findall(r"w:name=\"fig_", xml)))
print("sec_", len(re.findall(r"w:name=\"sec_", xml)))
print("PAGE", xml.count("PAGE"))
