import tkinter as tk
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import time

secimler = {}
matris = pd.read_csv('tablo_2.csv', index_col=0)
df = pd.read_csv('filtered_kategories_movie.csv')


frequent_itemsets = apriori(matris, min_support=0.2, use_colnames=True, max_len=2)

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)
print(rules)

class RecommendationTree:
    def __init__(self):

        self.tree = {}

    def add_rule(self, antecedent, consequent, confidence, antecedent_support, consequent_support):
        if antecedent not in self.tree:
            self.tree[antecedent] = []
        

        self.tree[antecedent].append({
            'consequents': consequent,
            'confidence': confidence,
            'antecedent support': antecedent_support,
            'consequent support': consequent_support
        })

    def get_rules(self, antecedent):
  
        return self.tree.get(antecedent, [])

    def print_tree(self):
        
        if not self.tree:
            print("Ağaç boş.")
            return
        
        for antecedent, rules in self.tree.items():
            print(f"Antecedent: {antecedent}")
            for rule in rules:
                print(f"  Consequent: {rule['consequents']}")
                print(f"  Confidence: {rule['confidence']}")
                print(f"  Antecedent Support: {rule['antecedent support']}")
                print(f"  Consequent Support: {rule['consequent support']}")



tree = RecommendationTree()


for _,rule in rules.iterrows():
    antecedent = rule['antecedents']
    consequent = rule['consequents']  
    confidence = rule['confidence']  
    antecedent_support = rule['antecedent support'] 
    consequent_support = rule['consequent support']  
    tree.add_rule(antecedent, consequent, confidence, antecedent_support, consequent_support)




root = tk.Tk()
root.title("Film Öneri Sistemi")
root.geometry("600x400")
root.configure(bg="#f0f8ff")  


window_width, window_height = 600, 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")


# Buton stili
button_style = {
    'font': ('Helvetica', 14, 'bold'),
    'bg': '#4682b4', 
    'fg': 'white',    # Beyaz yazı
    'activebackground': '#5f9ea0', 
    'activeforeground': 'white',
    'relief': 'groove',
    'bd': 2,
    'width': 25,
    'height': 2
}


frames = {}


def show_frame(frame_name):
    print("secimler sözlüğü içeriği4:", secimler)

    if frame_name == 'sonuc':
        güncelle_secim_text()
        
    for frame in frames.values():
        frame.pack_forget()
    frames[frame_name].pack(fill='both', expand=True)


def ana_ekran():
    frame = tk.Frame(root, bg="#f0f8ff", width=600, height=500)
    frames['ana_ekran'] = frame
    frame.pack_propagate(False)  
    frame.pack(fill='both', expand=True)


    orta_y = 250  


    btn_popüler = tk.Button(frame, text="Popüler Film Önerileri", 
                            command=lambda: [secim_yap('ilk_secim', 'Popüler Film Önerileri'),ikinci_sayfa(),show_frame('ikinci_sayfa')], 
                            **button_style)
    btn_popüler.place(relx=0.5, y=orta_y - 50, anchor="center")  


    btn_kişiselleştirilmiş = tk.Button(frame, text="Kişiselleştirilmiş Film Önerileri", 
                                       command=lambda: [secim_yap('ilk_secim', 'Kişiselleştirilmiş Film Önerileri'),kullanıcı_sec(), show_frame('kullanıcı_sec')], 
                                       **button_style)
    btn_kişiselleştirilmiş.place(relx=0.5, y=orta_y + 50, anchor="center") 
   
def ikinci_sayfa():

    frame = tk.Frame(root, bg="#f0f8ff")
    frames['ikinci_sayfa'] = frame

    btn_tur = tk.Button(frame, text="Film Türüne Göre Öneriler", command=lambda: [secim_yap('ikinci_secim', 'Film Türüne Göre Öneriler'),tur_sec(), show_frame('tur_sec')], **button_style)
    btn_tur.pack(pady=20)

    btn_isim = tk.Button(frame, text="Film İsmine Göre Öneriler", command=lambda: [secim_yap('ikinci_secim', 'Film İsmine Göre Öneriler'),film_sec(), show_frame('film_sec')], **button_style)
    btn_isim.pack(pady=20)

    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('ana_ekran'), **button_style)
    btn_geri.pack(pady=20)



def kullanıcı_sec():
    frame = tk.Frame(root, bg="#f0f8ff")
    frames['kullanıcı_sec'] = frame


    kullanıcılar = matris.index.tolist()


    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg="#f0f8ff", font=("Arial", 12))
    for kullanıcı in kullanıcılar:
        listbox.insert(tk.END, kullanıcı)
    listbox.pack(pady=10)

 
    def kullanıcı_seç():
        seçilen_index = listbox.curselection()
        if seçilen_index:
            seçilen_kullanıcı = listbox.get(seçilen_index)
            secim_yap('kullanıcı', seçilen_kullanıcı)
            ikinci_sayfa()
            show_frame('ikinci_sayfa')

    btn_seç = tk.Button(frame, text="Seç", command=kullanıcı_seç, **button_style)
    btn_seç.pack(pady=10)

   
    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('ana_ekran'), **button_style)
    btn_geri.pack(pady=20)


def tur_sec():

    frame = tk.Frame(root, bg="#f0f8ff")
    frames['tur_sec'] = frame
    unique_categories = set()
    df['genres'].dropna().apply(lambda x: unique_categories.update(x.split('|')))

    
    unique_categories = list(unique_categories)
   
    turler =  unique_categories.copy()

    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg="#f0f8ff", font=("Arial", 12))
    for tur in turler:
        listbox.insert(tk.END, tur)
    listbox.pack(pady=10)

    
    def tur_seç():
        seçilen_index = listbox.curselection()
        if seçilen_index:
            seçilen_tur = listbox.get(seçilen_index)
            secim_yap('seçilen_tur', seçilen_tur)
            film_oner()
            show_frame('film_oner')

    
    btn_seç = tk.Button(frame, text="Seç", command=tur_seç, **button_style)
    btn_seç.pack(pady=10)

 
    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('ikinci_sayfa'), **button_style)
    btn_geri.pack(pady=20)



def film_sec():
    print("deneme2")
    frame = tk.Frame(root, bg="#f0f8ff")
    frames['film_sec'] = frame

    if secimler.get('ilk_secim', '') == "Kişiselleştirilmiş Film Önerileri":
      
        kullanici_filmleri = [int(movie_id) for movie_id in matris.loc[secimler['kullanıcı']][matris.loc[secimler['kullanıcı']] >= 1].index.tolist()]
        # Film ID'lerine göre film isimlerini alalım
        filmler = []
        for movie_id in kullanici_filmleri:
            title = df[df['movieId'] == movie_id]['title'].values
            filmler.append((title[0], movie_id))

    elif secimler.get('ilk_secim', '') == "Popüler Film Önerileri":
      
        filmler = [(title, movie_id) for movie_id, title in zip(df['movieId'], df['title'])]

    
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg="#f0f8ff", font=("Arial", 12))
    for film in filmler:
        listbox.insert(tk.END, film)
    listbox.pack(pady=10)


    def film_seç():
        seçilen_index = listbox.curselection()
        
        if seçilen_index:
            seçilen_film_list_box = listbox.get(seçilen_index)
            film_id = seçilen_film_list_box[1]
            seçilen_film = film_id
            secim_yap('seçilen_film', seçilen_film)
            film_oner()
            show_frame('film_oner')


    btn_seç = tk.Button(frame, text="Seç", command=film_seç, **button_style)
    btn_seç.pack(pady=10)


    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('ikinci_sayfa'), **button_style)
    btn_geri.pack(pady=20)



def film_oner():
    

    if secimler.get('ilk_secim', '') =="Kişiselleştirilmiş Film Önerileri":
        if secimler.get('ikinci_secim', '') == "Film Türüne Göre Öneriler":
            if secimler.get('ikinci_secim', '') == "Film Türüne Göre Öneriler":
                kullanici_filmleri = matris.loc[secimler['kullanıcı']][matris.loc[secimler['kullanıcı']] >= 1].index.tolist()
              
                id_list = [int(item) for item in kullanici_filmleri]

          
                tur = secimler.get('seçilen_tur', '')

                for id in id_list:
                    id_frozen = frozenset([str(id)])
                  
                    kurallar_tree = tree.get_rules(id_frozen)
           
                    found_recommendation = False
                    
              
                    for row in kurallar_tree:
                        recommended_movie = row['consequents']
                        id = int(next(iter(recommended_movie)))
                        film_genres = df[df['movieId'] == id]['genres'].values[0]
                        
                        # Türleri '|' ile ayır
                        genres_list = film_genres.split('|')
                        
                   
                        if tur in genres_list and id not in id_list:
                            film_ismi = df[df['movieId'] == id]['title'].values[0]
                            oneri_film = film_ismi
                            found_recommendation = True
                            break  # İç döngüyü kır

                  
                    if found_recommendation:
                        break

                            
        elif secimler.get('ikinci_secim', '') == "Film İsmine Göre Öneriler":
            oneriler = rules[rules['antecedents'].apply(lambda x: str(secimler.get('seçilen_film', '')) in x)]

            en_yuksek_oneri = oneriler.sort_values(by='confidence', ascending=False).head(1)

            if not en_yuksek_oneri.empty:
                id = int(next(iter(en_yuksek_oneri.iloc[0]['consequents'])))
                movie_title = df.loc[df['movieId'] == id, 'title'].values
                oneri_film=movie_title
                confidence_degeri = en_yuksek_oneri.iloc[0]['confidence']
                print(f"Önerilen Film: {oneri_film}, Güven (Confidence): {confidence_degeri}")
            else:
                print("Seçilen film için bir öneri bulunamadı.")
    
    elif secimler.get('ilk_secim', '') =="Popüler Film Önerileri":
        if secimler.get('ikinci_secim', '') == "Film İsmine Göre Öneriler":
                
            oneriler = rules[rules['antecedents'].apply(lambda x: str(secimler.get('seçilen_film', '') )in x)]

            en_yuksek_oneri = oneriler.sort_values(by='confidence', ascending=False).head(1)

            if not en_yuksek_oneri.empty:
                id = int(next(iter(en_yuksek_oneri.iloc[0]['consequents'])))
                movie_title = df.loc[df['movieId'] == id, 'title'].values
                oneri_film=movie_title
                confidence_degeri = en_yuksek_oneri.iloc[0]['confidence']
                
        elif secimler.get('ikinci_secim', '') == "Film Türüne Göre Öneriler":
            start_time = time.perf_counter()
            selected_category = secimler.get('seçilen_tur', '')
            filtered_movies = df[df['genres'].str.contains(selected_category, na=False)]
            # movieId sütununu listeye çevir
            movie_list = filtered_movies['movieId'].tolist()

            max_support=0
                
            for movieId in movie_list :
                id_frozen = frozenset([str(movieId)])
                kurallar_tree = tree.get_rules(id_frozen)
                if kurallar_tree:
                    top_rule =max(kurallar_tree, key=lambda x: x['antecedent support'])
                    support_value= top_rule['antecedent support']

                    if support_value > max_support:
                        max_support= support_value
                        recommended_movie_id = movieId
            if recommended_movie_id:
                movie_title = df.loc[df['movieId'] == recommended_movie_id, 'title'].values
                oneri_film =movie_title
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"İşlem süresi: {elapsed_time:.4f} saniye")
           


    frame = tk.Frame(root, bg="#f0f8ff")
    frames['film_oner'] = frame


    secimler['önerilen_film'] = oneri_film
    label_öneri = tk.Label(frame, text=f"Önerilen Film: {secimler['önerilen_film']}", font=('Helvetica', 16), bg="#f0f8ff")
    label_öneri.pack(pady=20)


    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('ikinci_sayfa'), **button_style)
    btn_geri.pack(pady=20)

def sonuc():
    frame = tk.Frame(root, bg="#f0f8ff")
    frames['sonuc'] = frame

    global label
    label = tk.Label(frame, text="", font=('Helvetica', 16), bg="#f0f8ff")
    label.pack(pady=20)

    btn_geri = tk.Button(frame, text="Geri", command=lambda: show_frame('film_oner'), **button_style)
    btn_geri.pack(pady=20)

def güncelle_secim_text():
    print("secimler sözlüğü içeriği 2:", secimler)
    secim_text = f"İlk Seçim: {secimler.get('ilk_secim', '')}\n"
    print(secimler) 
    if 'kullanıcı' in secimler:
        secim_text += f"Kullanıcı: {secimler['kullanıcı']}\n"
    secim_text += f"İkinci Seçim: {secimler.get('ikinci_secim', '')}\n"
    secim_text += f"Seçilen Tür: {secimler.get('seçilen_tur', '')}\n"
    secim_text += f"Önerilen Film Türüne Göre: {secimler.get('önerilen_tur_film', '')}\n"
    secim_text += f"Seçilen Film: {secimler.get('seçilen_film', '')}\n"
    secim_text += f"Önerilen Film: {secimler.get('önerilen_film', '')}"
    label.config(text=secim_text)

# Seçimleri saklayan fonksiyon

def secim_yap(kategori, secim):
    secimler[kategori] = secim
    print(f"Kategori: {kategori}, Seçim: {secim}")
    

ana_ekran()

show_frame('ana_ekran')

root.mainloop()
