import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg


categories = ["ENG", "PHY", "CHEM", "MATHS","COMP"]
group1 = [93, 95, 98, 95,98]
group2 = [99, 96, 97,94,98 ]
group3 = [65, 55, 66, 57, 70]

x = np.arange(len(categories))
width = 0.25

plt.bar(x - width, group1, width, label="Marks obt")
plt.bar(x, group2, width, label="Topper's marks")
plt.bar(x + width, group3, width, label="Avg marks")

plt.title("Report graph")
plt.xlabel("SUBJECTS")
plt.ylabel("MARKS")
plt.xticks(x, categories)
plt.legend()


plt.savefig("bargraph.png")
plt.close()



with PdfPages("final_report.pdf") as pdf:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))  

    
    ax1.axis("off")
    table_data = [["Subjects", "Marks"], ["Eng",93 ], ["Phy", 95], ["Chem", 98],["Maths",95],["Comp",98]]
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