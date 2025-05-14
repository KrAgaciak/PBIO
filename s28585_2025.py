import random


def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length)) # Funkcja random.choices wybiera k przypadkowych liter z podanego ciągu


def insert_name(sequence, name):
    position = random.randrange(len(sequence) + 1)  # Nowa wersja używa randrange
    # position = random.randint(0, len(sequence)) # Losowo wybierana jest pozycja w ciągu z przedziału od 0 do długości ciągu
    return sequence[:position] + name + sequence[position:] # Ciąg dzielony jest na dwie części pomiędzy któymi wstawiane jest imie


def calculate_statistics(sequence):
    filtered_seq = ''.join(filter(lambda base: base in 'ACGT', sequence))  # Nowa wersja filtrowania
    #filtered_seq = ''.join([base for base in sequence if base in 'ACGT']) # ciąg jest filtrowany sprawdzając każdą pozycje po koleji czy znajduje się w podanyh znakach
    total = len(filtered_seq) # długość ciągu bez imienia
    stats = {base: round((filtered_seq.count(base) / total) * 100, 1) for base in 'ACGT'} # obliczanie procentowej zawartości każdego z podanych znaków
    cg_content = stats['C'] + stats['G'] # procentowa zawartość C+G
    return stats, cg_content # zwraca %


def save_to_fasta(id_seq, description, sequence_with_name):
    filename = f"{id_seq}.fasta" # Tworzona jest nazwa pliku z .fasta
    with open(filename, 'w') as file: # zapis do pliku
        file.write(f">{id_seq} {description}\n") # zapis id i opisu sekwaencji
        file.write(sequence_with_name + '\n') # zapis sekwencji z imieniem
    print(f"\nSekwencja została zapisana do pliku {filename}") # informacja o poprawnym zapisie do pliku


def main():
    # Pobieranie danych od użytkownika
    try:
        length = int(input("Podaj długość sekwencji: "))
    except ValueError:
        print("Podano nieprawidłową długość.")
        return

    # obrabianie danych od użytkownika
    id_seq = input("Podaj ID sekwencji: ").strip()
    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    # Generowanie i modyfikowanie sekwencji
    dna_sequence = generate_dna_sequence(length)
    sequence_with_name = insert_name(dna_sequence, name)

    # Obliczanie statystyk
    stats, cg_content = calculate_statistics(sequence_with_name)

    # Zapis do pliku FASTA
    save_to_fasta(id_seq, description, sequence_with_name)

    # Wyświetlanie statystyk
    print("Statystyki sekwencji:")
    for base in 'ACGT':
        print(f"{base}: {stats[base]}%")
    print(f"%CG: {cg_content}")


if __name__ == "__main__":
    main()