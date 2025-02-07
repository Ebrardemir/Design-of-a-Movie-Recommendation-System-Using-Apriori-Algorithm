import pandas as pd
import ast


def kategori_filtrele():
    movies_df = pd.read_csv("archive/movie.csv")

    exploded_df = movies_df.assign(genres=movies_df['genres'].str.split('|')).explode('genres')  # kategorilere ayırdım | lar ile kategorileri de ayırdım. 
    top_genres = exploded_df['genres'].value_counts().head(10).index # en popüler 10 kategoriyi belirledim

    # Burada, kategori sütununu str.contains ile kontrol ederek sadece belirlediğim 10 kategoriye sahip filmleri alıyorum
    top_genres_movies_df = movies_df[movies_df['genres'].apply(lambda x: any(genre in top_genres for genre in x.split('|'))) ]

    # Sadece en popüler 10 kategoriye sahip olan filmleri alıyorum
    top_genres_movies_df['genres'] = top_genres_movies_df['genres'].apply(lambda x: '|'.join([genre for genre in x.split('|') if genre in top_genres]))

    top_genres_movies_df.to_csv("kategories_movie.csv", index=False)

    print("Top 10 Kategoriler:") #ilk 10 kategori
    for genre in top_genres:
        print(genre)

def rating_filtrele():     #rating deki filmleri kategorilere ayrılmış filmlere göre filtreliyorum, 10 kategoriye göre
    movies_df = pd.read_csv('kategories_movie.csv')
    ratings_df = pd.read_csv('archive/rating.csv')

    valid_movie_ids = set(movies_df['movieId'])
    filtered_ratings_df = ratings_df[ratings_df['movieId'].isin(valid_movie_ids)] # movie de olup rating de olmayanları silme

    filtered_ratings_df = filtered_ratings_df.drop(columns=['timestamp'])

    filtered_ratings_df.to_csv('filtered_rating.csv', index=False)

    print("rating filtrele fonksiyonu çalıştı: 'filtered_rating_.csv'")

def tablo_olustur():
    df = pd.read_csv('filtered_rating.csv')

    # Her bir userId için izledikleri movieId'leri bir liste halinde gruplandır
    user_movie_df = df.groupby('userId')['movieId'].apply(list).reset_index()


    user_movie_df.columns = ['İzleyici', 'İzlenen Filmler']    # tablonun sütun isimleri
    user_movie_df.to_csv('izleyici_film_tablosu.csv', index=False)
    print("İzleyici-film tablosu oluşturuldu: 'izleyici_film_tablosu.csv'")

def kullanici_filtrele():
    df = pd.read_csv('izleyici_film_tablosu.csv')

    df['İzlenen Filmler'] = df['İzlenen Filmler'].apply(eval)# 'İzlenen Filmler' sütununu liste olarak alıyoruz bunun üzerinden işlemler yapıclak

    filtered_df = df[df['İzlenen Filmler'].apply(len) >= 1500] 
    filtered_df.to_csv('filtrelenmis_izleyici_film_tablosu.csv', index=False)

    print("kullanıcı filtrelendi: 'filtrelenmis_izleyici_film_tablosu.csv'")

def film_filtrele():
    df = pd.read_csv("filtrelenmis_izleyici_film_tablosu.csv")

    df['İzlenen Filmler'] = df['İzlenen Filmler'].apply(ast.literal_eval)# İzlenen filmleri satır bazında listeye dönüştürmw böylece filtreleme yapabiliyorum

    exploded_df = df.explode('İzlenen Filmler') #tüm filmleri ayırıyorum
    film_counts = exploded_df['İzlenen Filmler'].value_counts()

    popular_films = film_counts[film_counts >= 300].index
    filtered_df = exploded_df[exploded_df['İzlenen Filmler'].isin(popular_films)]

    result_df = filtered_df.groupby('İzleyici')['İzlenen Filmler'].apply(list).reset_index()

    result_df.to_csv("filtered_filtrelenmis_izleyici_film_tablosu.csv", index=False)

    print("film filtreleme yapildi")

def eslestir():
    movies_df = pd.read_csv('kategories_movie.csv')
    user_movies_df = pd.read_csv('filtered_filtrelenmis_izleyici_film_tablosu.csv')

    user_movies_df['İzlenen Filmler'] = user_movies_df['İzlenen Filmler'].apply(eval) #listeye çevirme apply(eval)
    watched_movies = set(movie for movies in user_movies_df['İzlenen Filmler'] for movie in movies)# Tüm izlenen filmleri tek bir set halinde topla

    filtered_movies_df = movies_df[movies_df['movieId'].isin(watched_movies)]
    filtered_movies_df.to_csv('filtered_kategories_movie.csv', index=False)

    print("filmler tabloya göre filtrelendi: 'filtered_kategories_movie.csv'")

def tablo_2():
    movies_df = pd.read_csv('filtered_kategories_movie.csv')
    user_movies_df = pd.read_csv('filtered_filtrelenmis_izleyici_film_tablosu.csv')

    user_movies_df['İzlenen Filmler'] = user_movies_df['İzlenen Filmler'].apply(eval)

    # Tüm izleyici ve film eşleşmelerini içeren bir DataFrame oluşturma
    user_movie_data = []
    for _, row in user_movies_df.iterrows():
        user_id = row['İzleyici']
        watched_movies = row['İzlenen Filmler']
        for movie_id in watched_movies:
            if movie_id in movies_df['movieId'].values:  # Filmin kategories_movie.csv'de olup olmadığını kontrol et
                user_movie_data.append((user_id, movie_id))

    user_movie_df = pd.DataFrame(user_movie_data, columns=['userId', 'movieId'])

    user_movie_matrix = user_movie_df.pivot_table(index='userId', columns='movieId', aggfunc='size', fill_value=0) #pivot tablosu olarak oluşturdum

    # Sütun isimlerini film ID'lerine göre düzenleme
    user_movie_matrix.index.name = 'İzleyiciler'
    user_movie_matrix.columns = [f'{int(col)}' for col in user_movie_matrix.columns]

    user_movie_matrix.to_csv('tablo_2.csv')

    print("tablo 2 olusturuldu: tablo_2.csv ")

kategori_filtrele()
rating_filtrele()
tablo_olustur()
kullanici_filtrele()
film_filtrele()
eslestir()
tablo_2()