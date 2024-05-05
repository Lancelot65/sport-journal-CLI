import json
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
import numpy as np

DATA_FILE = "sessions.json"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {} 
    
def attendre_entre():
    input("Appuyez sur Entrée pour continuer...")

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_exercise(data, exercise_name):
    if not exercise_name in data:
        data[exercise_name] = []
        save_data(data)
        print(f"Exercice '{exercise_name}' ajouté avec succès.")
        attendre_entre()

def print_exercise(data):
    for key in data.keys():
        print(key)
    attendre_entre()

def add_session(data, exercise_name, repetitions, sets, date):
    if exercise_name in data:
        data[exercise_name].append({"repetitions": repetitions, "sets": sets, "date" : date})
        save_data(data)
        print(f"Session ajoutée avec succès dans '{exercise_name}' avec {sets} séries de {repetitions} répétitions le {date}")
    else:
        print(f"Erreur : l'exercice '{exercise_name}' n'existe pas.")
    attendre_entre()

def plot_evolution(data, exercise_name):
    repetitions_over_time = []
    series_over_time = []
    dates = []

    if exercise_name in data:
        for session in data[exercise_name]:
            repetitions_over_time.append(session["repetitions"])
            series_over_time.append(session["sets"])
            dates.append(datetime.strptime(session["date"], "%Y:%m:%d"))

        # Trier les données par dates
        sorted_indexes = np.argsort(dates)
        dates = np.array(dates)[sorted_indexes]
        repetitions_over_time = np.array(repetitions_over_time)[sorted_indexes]
        series_over_time = np.array(series_over_time)[sorted_indexes]

        # Largeur des barres
        bar_width = 0.3
        # Position des barres pour les séries
        bar_positions = np.arange(len(dates))

        fig, ax = plt.subplots()

        # Placer les barres pour les séries
        ax.bar(bar_positions - bar_width/2, series_over_time, bar_width, color='r', alpha=0.5, label='Séries')

        # Placer les barres pour les répétitions par série
        ax.bar(bar_positions + bar_width/2, repetitions_over_time, bar_width, color='g', alpha=0.5, label='Répétitions par série')

        # Ajouter les croix pour le produit des répétitions et des séries
        ax.scatter(bar_positions, repetitions_over_time * series_over_time, color='b', marker='x', label='Répétitions totales')

        # Ajouter les lignes en pointillés entre les croix
        for i in range(len(bar_positions)-1):
            ax.plot([bar_positions[i], bar_positions[i+1]], 
                    [repetitions_over_time[i] * series_over_time[i], repetitions_over_time[i+1] * series_over_time[i+1]], 
                    'b--')

        ax.set_xticks(bar_positions)
        ax.set_xticklabels([date.strftime("%Y-%m-%d") for date in dates], rotation=45, ha='right')

        ax.set_xlabel('Sessions')
        ax.set_ylabel('Quantité')
        ax.legend()

        fig.tight_layout()
        plt.title(f"Évolution du nombre de répétitions et de séries pour l'exercice '{exercise_name}'")
        plt.show()
        return
    print(f"Erreur : l'exercice '{exercise_name}' n'existe pas.")
    
def main():
    data = load_data()
    while True:
        clear_terminal()
        print("Menu:")
        print("1. Ajouter une session d'entraînement")
        print("2. Afficher l'évolution du nombre de répétitions pour un exercice")
        print("3. Option avancer")
        print("4. Quitter")
        choice = input("Choisissez une option: ")

        if choice == "1":
            exercise_name = input("Entrez le nom de l'exercice: ")
            if exercise_name not in data:
                print(f"exercice '{exercise_name}' n'existe pas")
                attendre_entre()
                continue
            
            sets = int(input("Nombre de séries: "))

            repetitions = int(input("Nombre de répétitions : "))
            date = input("Date de la série (YYYY:MM:JJ ou auto (o)) : ")
            if date == "o":
                date = datetime.now().strftime("%Y:%m:%d")
            add_session(data, exercise_name, repetitions, sets, date)

        elif choice == "2":
            exercise_name = input("Entrez le nom de l'exercice: ")
            plot_evolution(data, exercise_name)
            attendre_entre()
            

        elif choice == "3":
            clear_terminal()

            print("1. Ajouter un nouvel exercice")
            print("2. Afficher les exercices déjà présent")
            choice = input("Choisissez une option : ")

            if choice == "1":
                exercise_name = input("Entrez le nom de l'exercice: ")
                add_exercise(data, exercise_name)
            elif choice == "2":
                print_exercise(data)
            else:
                print("Option invalide. Veuillez choisir une option valide.")
                input("Appuyez sur Entrée pour continuer...")

        elif choice == "4":
            sys.exit()

        else:
            print("Option invalide. Veuillez choisir une option valide.")
            input("Appuyez sur Entrée pour continuer...")  # Pause pour continuer après un message d'erreur

if __name__ == "__main__":
    main()
