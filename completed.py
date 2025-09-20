import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

#for bar graph
categories = ["ENG", "PHY", "CHEM", "MATHS","COMP"]
group1 = [93, 95, 98, 95,98]
group2 = [99, 96, 97,94,98 ]
group3 = [65, 55, 66, 57, 70]

x = np.arange(len(categories))
width = 0.25

#for teeno bars ki position
plt.bar(x - width, group1, width, label="Marks obt")
plt.bar(x, group2, width, label="Topper's marks")
plt.bar(x + width, group3, width, label="Avg marks")


plt.title("Report graph", fontsize=20, fontweight="bold", fontstyle="italic", fontname="Times New Roman")
plt.xlabel("SUBJECTS")
plt.ylabel("MARKS")
plt.xticks(x, categories)
plt.legend()


plt.savefig("bargraph.png")
plt.close()



with PdfPages("final_report.pdf") as pdf:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))  

    
    ax1.axis("off")
    
    ax1.text(0.5, 1.05, "REPORT CARD ", #FOR MAIN HEADING 
         ha="center", va="bottom",
         fontsize=14, fontweight="bold")
    ax1.text(0.0, 0.98, "Name:", # coordinates
         ha="left", va="bottom",
         fontsize=8, fontweight="bold")
    ax1.text(0.2, 0.98, "Tanmay Nirmal",
         ha="center", va="bottom",
         fontsize=8, fontweight="bold")   
    ax1.text(0.04, 0.94, "Class :",
         ha="center", va="bottom",
         fontsize=8, fontweight="bold")
    ax1.text(0.15, 0.94, "XII-A",
         ha="center", va="bottom",
         fontsize=8, fontweight="bold")                
    table_data = [["Subjects", "Marks"], ["Eng",93 ], ["Phy", 95], ["Chem", 98],["Maths",95],["Comp",98]] #for table
    table = ax1.table(cellText=table_data, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    ax2.axis("off")
    img = mpimg.imread("bargraph.png")
    ax2.imshow(img)

    pdf.savefig(fig)
    plt.close(fig)

print(" PDF 'final_report.pdf' created.")
