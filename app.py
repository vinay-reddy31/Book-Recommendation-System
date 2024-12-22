from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
print(popular_df.head())
print(popular_df.columns)

pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_scores.pkl','rb'))

books_list=books['Book-Title'].values
print(books_list)

app=Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    query = request.args.get('query', '').lower()
    suggestions = [book for book in books_list if query in book.lower()]
    return jsonify(suggestions[:10])  # Return only the top 10 matches

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        print(pt.index[i[0]])
        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)


if __name__=="__main__":
    app.run(debug=True)

