# 📊 Bank Marketing Campaign — Funnel & Conversion Analysis

> Task 3 of 3 · Data Science & Analytics Internship · [Future Interns]  
> Author: Nkosinathi Mathenjwa  
> Dataset: UCI Bank Marketing Dataset (45,211 records)  
> Tools: Python · Pandas · Matplotlib

---

📌 Project Overview

This project analyses a real-world bank telemarketing campaign to understand where conversions happen, where they drop off, and why.

The goal is to answer questions like:
- Which customers are most likely to subscribe to a term deposit?
- Which months, channels, and segments perform best?
- Where is the campaign wasting resources?

The final output is a **fully custom dark-mode landscape dashboard** built entirely in Python — no BI tools, no shortcuts.

---

📂 Project Structure

bank-marketing-dashboard/
│
├── bank_dashboard.py       
├── bank-full.csv           
├── bank_marketing_dashboard.png  
└── README.md               
```

---

🚀 How to Run

1. Clone the repo
```
clone repo
cd bank-marketing-dashboard
```

2. Install dependencies
```
bash
pip install pandas matplotlib
```

3. Run the dashboard
``
bash
python3 bank_dashboard.py
```

The dashboard PNG will be saved in the same folder automatically.

---

📊 Dashboard Panels

| Panel                     | What it shows |

| KPI Cards                 | Total contacts, conversions, overall rate, avg call duration |
| Contact Channel           | Conversion rate by cellular vs telephone vs unknown |
| Monthly Trends            | Which months peak and which waste budget |
| Campaign Contacts         | How conversion drops after 2+ calls to the same person |
| Job Type                  | Which professions convert best (students, retirees lead) |
| Education Level           | Tertiary vs secondary vs primary conversion rates |
| Housing Loan Impact       | Loan vs no-loan conversion comparison |
| Key Drop-off Risks        | Summary of the 5 biggest conversion leaks |

---

🔍 Key Findings

- 📅 **May accounts for 30% of all calls** but only converts at **6.7%** — the worst month in the dataset
- ✅ **Previously successful contacts convert at 64.7%** — re-targeting them first is the highest-ROI move
- 📞 **Call duration is the strongest predictor** — calls over 10 minutes convert at 48% vs 0.2% under 1 minute
- 🎓 **Students (28.7%) and retirees (22.8%)** are the most convertible job segments
- 🏠 **No housing loan = 2× more likely to subscribe** (16.7% vs 7.7%)
- 📵 **Calling someone 3+ times hurts conversion** — diminishing returns kick in fast
- ❓ **Unknown contact method = 4.1% conversion** — poor data quality is silently killing results

---

💡 Recommendations

1. **Shift campaign timing** away from May — focus on March, September, October, and December
2. **Re-target previous successes first** before cold outreach
3. **Train agents to extend calls past 5 minutes** — engagement time directly drives conversion
4. **Stop after 2 contact attempts** — more calls reduce conversion probability
5. **Fix contact data quality** — classify unknown contact methods to recover hidden conversions
6. **Focus targeting on students and retirees** — highest conversion segments are currently underserved

---

## 📁 Dataset

**UCI Bank Marketing Dataset**  
Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing)  
Records: 45,211  

---

🛠️ Tech Stack

| Tool              | Purpose 

| Python 3          | Core language 
| Pandas            | Data loading, cleaning, aggregation 
| Matplotlib        | All charts and dashboard layout 
| GridSpec          | Multi-panel landscape layout 
| FancyBboxPatch    | Custom styled card elements 

---

🙋 About Me

**Nkosinathi Mathenjwa**    
Passionate about turning raw data into decisions.

- 🔗 [LinkedIn](https://www.linkedin.com/in/nkosinathi-mathenjwa-266ba0235/)
- 💻 [GitHub](https://github.com/MTHI6223)

---

