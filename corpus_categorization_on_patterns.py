# автоматичний пошук та категоризація військової лексики китайської мови на основі корпусу
import pandas as pd
import re
import matplotlib.pyplot as plt
# корпус
with open("mil_corpus.txt", 'rt', encoding='utf-8') as f1:
	full_text = f1.read()
# Шаблони для виявлення термінів
templates = {
# Класифікація за типом зброї, техніки та систем:
"系统类术语": r'([\u4e00-\u9fa5]{2,6}(系统|平台|设施))',
"导弹类术语": r'((空|地|海)?对(空|地|海)?(导弹|系统|平台|发射器|雷达|导引))',
"战术武器": r'([\u4e00-\u9fa5]{2,7}(战车|坦克|装甲车|自行炮|步兵战车|反坦克导弹|导弹|武器|飞弹|弹药))',
"飞机类术语": r'([\u4e00-\u9fa5]{2,4}(轰炸机|战斗机|运输机|加油机|侦察机|无人机))',
"舰船类术语": r'([\u4e00-\u9fa5]{2,4}(战舰|驱逐舰|潜艇|航母|护卫舰|巡洋舰|潜舰|舰艇|航舰|驱逐舰|登陆舰|运输舰|军舰))',
"火炮类术语": r'([\u4e00-\u9fa5]{2,4}(火炮|加农炮|自走炮|反舰导弹|火箭炮|多管火箭|运载火箭|火箭))',
"防空类术语": r'([\u4e00-\u9fa5]{2,4}(防空|导弹防御|防空导弹|防空系统|雷达|SAM))',
"雷达类术语": r'([\u4e00-\u9fa5]{2,4}(雷达|跟踪|探测|反辐射|防空雷达|气象雷达))',
"指挥中心类术语": r'[^\d]([\u4e00-\u9fa5]{2,6}(指挥中心|作战指挥|战术指挥|战略指挥|指挥所|指挥|单位|中心|基地|司令部|委员会|机构|组织|管制))',
"直升机类术语": r'([\u4e00-\u9fa5]{2,4}(直升机|武装直升机|攻击直升机|运输直升机))',
"部队类术语": r'([\u4e00-\u9fa5]{2,5}(部队|步兵|装甲兵|炮兵|特种兵|空降兵|海军陆战队|防空兵|战略支援部队))',
"军事人员": r'([\u4e00-\u9fa5]{2,}(人员|军官|指挥官|兵力|参谋|士官|上士|中士|下士|士兵))',
# Шаблони для виявлення термінів, пов’язаних з військовою стратегією, операціями:
"战略类术语": r'([\u4e00-\u9fa5]{2,4}(战略|战术|反应|攻势|防御|部署|作战计划|战略目标|打击能力))',
"作战类术语": r'([\u4e00-\u9fa5]{2,5}(战役|作战|战斗|反恐|反渗透|防御作战|进攻作战|围歼|突击|冲击|打击|攻击|射击|轰炸|袭击|突袭|袭扰|空袭|进攻|歼击))',
"特种兵类术语": r'([\u4e00-\u9fa5]{2,4}(特种兵|特种作战|反恐部队|特战队|侦察队|潜伏任务|城市战))',
"战术工具类术语": r'([\u4e00-\u9fa5]{2,4}(战术|机动|隐蔽|战斗小组|电子战|远程打击|精确打击|情报|侦察|监视|搜索))',
"联合作战类术语": r'([\u4e00-\u9fa5]{2,4}(联合战役|联合指挥|空地一体|海空联合|多维作战|联合作战计划|训练|战备|演习))',
# Шаблони для термінів з військовими технічними аспектами (наприклад, матеріали, технології):
"人工智能类术语": r'([\u4e00-\u9fa5]{2,4}(人工智能|机器学习|深度学习|大数据|无人系统|智能武器))',
"技术类术语": r'([\u4e00-\u9fa5]{2,4}(高超音速|隐形技术|激光武器|电磁炮|量子通信|网络战|电子战))',
"军事科技类术语": r'([\u4e00-\u9fa5]{2,4}(军事技术|武器研发|先进技术|军事科研|国防科技|军工企业))',
# Шаблони для термінів, що стосуються військових об'єктів (типи баз, споруд):
"军事基地类术语": r'([\u4e00-\u9fa5]{2,4}(军事基地|战术基地|防空基地|指挥中心|弹药库|军舰停泊港))',
"战场类术语": r'([\u4e00-\u9fa5]{2,4}(前线|战场|阵地|指挥所|炮兵阵地|空中打击点|防线))'
}
# Виявлення термінів
print("Витяг термінів за шаблонами...")
found_terms = []
found_terms2 = []
seen_terms = set()

for label, pattern in templates.items():
    matches = re.findall(pattern, full_text)
    for match in matches:
        found_terms.append((match[0], label))
        if match[0] not in seen_terms:
            found_terms2.append((match[0], label))
            seen_terms.add(match[0])

# Збереження у DataFrame
df = pd.DataFrame(found_terms, columns=["Термін", "Шаблон"])
df2 = pd.DataFrame(found_terms2, columns=["Термін", "Шаблон"])
# Групування
stats = df["Шаблон"].value_counts()
print("📊 Статистика шаблонів: \n", stats)
# Побудова графіка
plt.rcParams['font.sans-serif'] = ['SimHei']  # для китайських ієрогліфів
plt.figure(figsize=(8, 5))
stats.plot(kind='bar', color='skyblue')
plt.title("Term Distribution by Template")
plt.xlabel("Template Type")
plt.ylabel("Quantity")
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig("C:\\Users\\davin\\Desktop\\Статистика_шаблонів.png", dpi=300, bbox_inches='tight')
print("🖼️ Графік збережено як 'Статистика_шаблонів.png'")
plt.show()
# Збереження результатів на диск
#df2.to_csv("C:\\Users\\davin\\Desktop\\військові_терміни_з_новин.csv", index=False, encoding='utf-8')
#print("💾 Збережено 'військові_терміни_з_новин.csv'")

# 🔢 Підрахунок частоти термінів
term_counts = df["Термін"].value_counts()
# 📌 Вибір термінів, які зустрічаються більше 3 разів
frequent_terms = term_counts[term_counts > 4]
# 📋 Об'єднуємо часті терміни з лейблами з df2
df2_filtered = df2[df2["Термін"].isin(frequent_terms.index)].copy()
# ➕ Додаємо колонку "Кількість"
df2_filtered["Кількість"] = df2_filtered["Термін"].map(frequent_terms)
# 🔽 Сортуємо за спаданням
df2_filtered.sort_values(by="Кількість", ascending=False, inplace=True)
df2_filtered.to_csv("C:\\Users\\davin\\Desktop\\військові_терміни_частотні.csv", index=False, encoding='utf-8')
print("💾 Збережено 'військові_частотні_терміни.csv'")
# 📊 Побудова графіка частотних термінів
plt.figure(figsize=(10, 6))
df2_filtered = df2_filtered.head(25)#кількість термінів на графіку (наприклад, топ-25)
plt.barh(df2_filtered["Термін"], df2_filtered["Кількість"], color='orange')
plt.xlabel("Number of occurrences of terms")
plt.ylabel("Term")
plt.title("Most frequent military terms in the corpus")
plt.gca().invert_yaxis()  # Щоб найчастіші були вгорі
plt.grid(axis='x', linestyle='--', alpha=0.5)
# Встановлення шрифту для китайських ієрогліфів
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.tight_layout()
plt.savefig("C:\\Users\\davin\\Desktop\\військові_терміни_частотні.png", dpi=300, bbox_inches='tight')
print("🖼️ Графік збережено як 'військові_терміни_частотні.png'")
plt.show()
