import tubo

text = ['italy', 'germany', 'brazil', 'france', 'england',
    'argentina', 'peru', 'united states', 'australia',
    'sweden', 'china', 'poland', 'portugal']

def capitalize(lines):
    for line in lines:
        for word in line.split(","):
            yield word.capitalize()

def filter_wordwith_i(words):
    for word in words:
        if 'i' in word:
          yield word

output = tubo.pipeline(
    text,
    filter_wordwith_i,
    capitalize,
)

print list(output)
