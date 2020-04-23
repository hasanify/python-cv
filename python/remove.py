bad_words = ['Personal', 'Information', 'Projects', 'Internship', 'Technologies']

with open('test.txt') as oldfile, open('newfile.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)