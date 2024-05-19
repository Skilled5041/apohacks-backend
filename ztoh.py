import cohere

co = cohere.Client("")
stream = co.chat_stream(
  model='command-r-plus',
  message='''You are a translator who translates from zombie speak to english. . Some common translations of words are : "A": "grr",
        "B": "argh",
        "C": "ugh",
        "D": "rawr",
        "E": "brr",
        "F": "gah",
        "G": "urr",
        "H": "blur",
        "I": "hmm",
        "J": "zzz",
        "K": "rarr",
        "L": "blargh",
        "M": "snar",
        "N": "arg",
        "O": "mur",
        "P": "grar",
        "Q": "urgh",
        "R": "blurr",
        "S": "snarl",
        "T": "garr",
        "U": "hur",
        "V": "braar",
        "W": "snur",
        "X": "grargh",
        "Y": "grur",
        "Z": "arrgh",
        " ": "hrr"
''',
  temperature=0,
  chat_history=[{"role": "User", "message": "Translate \"gruhgraler\" into english"}, {"role": "Chatbot", "message": "\"eat brains\""}, {"role": "User", "message": "Translate \"gruhgraler\" into english"}, {"role": "Chatbot", "message": "\"eat brains\""}],
  prompt_truncation='AUTO',
  connectors=[{"id":"web-search","options":{"site":"https://www.sparknotes.com/lit/indian-horse/chapter-summaries/"}}]
)

for event in stream:
  if event.event_type == "text-generation":
    print(event.text, end='')