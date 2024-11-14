from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "images"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarah_birthday.db'
db = SQLAlchemy(app)

# Define the MenuItem model
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_fr = db.Column(db.String(100), nullable = False)
    name_de = db.Column(db.String(100), nullable = False)
    description_fr = db.Column(db.String(200), nullable = False)
    description_de = db.Column(db.String(200), nullable = False)
    category_fr = db.Column(db.String(50), nullable = True)
    category_de = db.Column(db.String(50), nullable = True)
    image_path = db.Column(db.String(100), nullable = False)

def create_tables():
    db.create_all()
    # Insert sample data only if table is empty
    if not MenuItem.query.first():
        sample_items = [
            MenuItem(
                name_fr='Macaroni de chalet',
                name_de='Hüttennudeln',
                description_fr="Un classique de la cuisine alpine : ces macaronis de chalet sont cuisinés dans une crème onctueuse, accompagnés de lardons de chez Pittet.",
                description_de="Ein Klassiker der alpinen Küche: Diese Hüttennudeln werden in einer cremigen Sauce mit Speck von Pittet zubereitet.",
                category_fr='Plats',
                category_de='Gerichte',
                image_path='images/macaroni.png'
            ),
            MenuItem(
                name_fr='Plateau de fromages',
                name_de='Käseplatte',
                description_fr="Ce plateau de fromages, c'est comme une randonnée en montagne... sans l'effort ! Au lait cru, chaque morceau est une invitation à voyager des pâturages d'altitude aux caves sombres où il a mûri en secret.",
                description_de="Diese Käseplatte ist wie eine Bergwanderung... nur ohne Anstrengung! Aus Rohmilch, jedes Stück lädt zu einer Reise von den Höhenweiden zu den dunklen Kellern ein, in denen es heimlich gereift ist.",
                category_fr='Apéritifs',
                category_de='Vorspeisen',
                image_path='images/fromages.png'
            ),
            MenuItem(
                name_fr='Saucisson sec de bœuf',
                name_de='Rindfleisch-Salami',
                description_fr="Séché à l'air pur des montagnes, ce saucisson de bœuf offre une texture ferme et des saveurs riches, rehaussées de subtiles épices.",
                description_de="An der klaren Bergluft getrocknet, bietet dieser Rindfleisch-Salami eine feste Textur und reiche Aromen, verfeinert mit subtilen Gewürzen.",
                category_fr='Apéritifs',
                category_de='Vorspeisen',
                image_path='images/dry_sausage.png'
            ),
            MenuItem(
                name_fr='Jambon blanc',
                name_de='Weißer Schinken',
                description_fr="Délicatement salé et d'une tendreté incomparable, ce jambon issu de la maison Stuby te fera frissonner.",
                description_de="Zart gesalzen und unvergleichlich zart, dieser Schinken aus dem Hause Stuby wird dir eine Gänsehaut verleihen.",
                category_fr='Apéritifs',
                category_de='Vorspeisen',
                image_path='images/jambon.png'
            ),
            MenuItem(
                name_fr='Chips',
                name_de='Chips',
                description_fr="Fines et croustillantes pour un plaisir gourmand et irrésistible à chaque bouchée.",
                description_de="Fein und knusprig für ein köstliches und unwiderstehliches Vergnügen bei jedem Bissen.",
                category_fr='Apéritifs',
                category_de='Vorspeisen',
                image_path='images/chips.png'
            ),
            MenuItem(
                name_fr='Cacahuètes',
                name_de='Erdnüsse',
                description_fr="Croquantes et légèrement salées, idéales pour augmenter son body fat.",
                description_de="Knackig und leicht gesalzen, ideal um das Körperfett zu erhöhen.",
                category_fr='Apéritifs',
                category_de='Vorspeisen',
                image_path='images/peanut.png'
            ),
            MenuItem(
                name_fr='Bière Cardinal',
                name_de='Bier Cardinal',
                description_fr="Une bière blonde suisse, légère et rafraîchissante, avec des notes de malt subtiles et une mousse délicate. Parfaite pour se réconforter après un match de Gottéron.",
                description_de="Ein leichtes, erfrischendes Schweizer Lagerbier mit subtilen Malznoten und feinem Schaum. Perfekt zur Erholung nach einem Gottéron-Spiel.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/beer.png'
            ),
            MenuItem(
                name_fr='Vin blanc',
                name_de='Weißwein',
                description_fr="Un vin blanc frais et fruité, aux arômes délicats d'agrumes et de fleurs blanches.",
                description_de="Ein frischer und fruchtiger Weißwein mit zarten Aromen von Zitrusfrüchten und weißen Blüten.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/white_wine.png'
            ),
            MenuItem(
                name_fr='Vin rouge',
                name_de='Rotwein',
                description_fr="Un vin rouge élégant et corsé, aux arômes profonds de fruits rouges et d'épices.",
                description_de="Ein eleganter und kräftiger Rotwein mit tiefen Aromen von roten Früchten und Gewürzen.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/red_wine.png'
            ),
            MenuItem(
                name_fr='Sirops',
                name_de='Sirups',
                description_fr="Des sirops riches en saveurs fruitées, parfaits pour créer des boissons rafraîchissantes rappelant ton enfance.",
                description_de="Fruchtige Sirups, ideal für erfrischende Getränke, die an deine Kindheit erinnern.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/sirup.png'
            ),
            MenuItem(
                name_fr='Eau gazeuse',
                name_de='Sprudelwasser',
                description_fr="Une eau naturellement pétillante de la source des Marécottes.",
                description_de="Ein natürlich sprudelndes Wasser aus der Quelle der Marécottes.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/spark_water.png'
            ),
            MenuItem(
                name_fr='Eau plate',
                name_de='Stillwasser',
                description_fr="Pure et légère, cette eau cristalline est un diurétique idéal.",
                description_de="Rein und leicht, dieses kristallklare Wasser ist ein ideales Diuretikum.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/water.png'
            ),
            MenuItem(
                name_fr='Porto',
                name_de='Portwein',
                description_fr="Doux et généreux, aux saveurs de fruits mûrs avec une subtile note boisée.",
                description_de="Weich und großzügig, mit Aromen reifer Früchte und einer feinen Holznote.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/porto.png'
            ),
            MenuItem(
                name_fr='Pastis',
                name_de='Pastis',
                description_fr="La boisson incontournable des joueurs et joueuses de boules.",
                description_de="Das unverzichtbare Getränk für Boules-Spieler und -Spielerinnen.",
                category_fr='Boissons',
                category_de='Getränke',
                image_path='images/pastis.png'
            ),
            MenuItem(
                name_fr='Desserts de Tati',
                name_de='Tatis Desserts',
                description_fr="Des desserts authentiques faits maison, élaborés dans la plus grande tradition helvétique.",
                description_de="Authentische, hausgemachte Desserts, die nach bester helvetischer Tradition zubereitet werden.",
                category_fr='Desserts',
                category_de='Desserts',
                image_path='images/cakes.png'
            ),
            MenuItem(
                name_fr='Banana Bread',
                name_de='Bananenbrot',
                description_fr="Un cake moelleux à la banane, directement inspiré des saveurs de Salgesch.",
                description_de="Ein weicher Bananenkuchen, direkt inspiriert von den Aromen aus Salgesch.",
                category_fr='Desserts',
                category_de='Desserts',
                image_path='images/banana_bre.png'
            )
        ]
        db.session.bulk_save_objects(sample_items)
        db.session.commit()

with app.app_context():
    create_tables()

@app.route('/')
def menu():
    items = MenuItem.query.all()
    categories = sorted({item.category_fr for item in items if item.category_fr})
    menu_title = 'Menu'
    category_title = 'Catégorie'
    filter_title = 'Tout'

    items_data = [{
        'name': item.name_fr,
        'description': item.description_fr,
        'category': item.category_fr,
        'image_path': item.image_path
    } for item in items]

    selected_language = session.get('lang', 'fr')

    return render_template('menu.html', 
                           items=items_data,
                           categories=categories, 
                           menu_title = menu_title,
                           category_title = category_title,
                           filter_title = filter_title,
                           language_route = '/fr',
                           selected_language = selected_language)

@app.route('/de')
def menu_de():
    items = MenuItem.query.all()
    categories = sorted({item.category_de for item in items if item.category_de})
    menu_title = 'Menü'
    category_title = 'Kategorie'
    filter_title = 'Alles'
    items_data = [{
        'name': item.name_de,
        'description': item.description_de,
        'category': item.category_de,
        'image_path': item.image_path
    } for item in items]

    selected_language = session.get('lang', 'de')


    return render_template('menu.html',
                            items=items_data, 
                            categories=categories, 
                            menu_title = menu_title,
                            category_title = category_title,
                            filter_title = filter_title,
                            language_route='/de',
                            selected_language = selected_language)

@app.route('/fr/filter', methods=['GET'])
def filter_items_fr():
    category = request.args.get('category')
    if category:
        items = MenuItem.query.filter_by(category_fr=category).all()
    else:
        items = MenuItem.query.all()

    items_data = [{
        'name': item.name_fr,
        'description': item.description_fr,
        'category': item.category_fr,
        'image_path': item.image_path
    } for item in items]

    return jsonify(items_data)


@app.route('/de/filter', methods=['GET'])
def filter_items_de():
    category = request.args.get('category')
    if category:
        items = MenuItem.query.filter_by(category_de=category).all()
    else:
        items = MenuItem.query.all()

    items_data = [{
        'name': item.name_de,
        'description': item.description_de,
        'category': item.category_de,
        'image_path': item.image_path
    } for item in items]

    return jsonify(items_data)


@app.route('/generate_qr_code')
def save_qr_code():
    # Generate the URL for the root route
    url = url_for('menu', _external=True)  # _external=True generates the full URL
    qr = qrcode.make(url)
    
    # Save the QR code to a file in the static directory
    qr_path = 'static/qr_code.png'
    qr.save(qr_path)
    
    return f"QR code saved as {qr_path}. You can print it from the file."

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    if lang == 'fr':
        return redirect(url_for('menu'))
    elif lang == 'de':
        return redirect(url_for('menu_de'))
    return redirect(url_for('menu'))  # Default to French


if __name__ == '__main__':
    app.run(debug=True)