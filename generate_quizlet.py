from random import shuffle
import codecs
import sys

stop_words = "0123456789.,;:'!@#$%^&*()_-=+<>?"

def generate_quizlet(class_name, part_id, mode="new", num_new_quest=10, num_old_quest=5):
    root_path = './data/' + class_name
    input_file = codecs.open(root_path + '_collection.txt', 'r', 'utf8')
    output_file = codecs.open(root_path + '_quizlet.txt', 'w', 'utf8')
    keyword_file = codecs.open(root_path + '_keyword.txt', 'r', 'utf8')
    #attention: for codes, the last character should be ignored

    #collect keywords
    keywords = {}
    words_canvas = {}
    input_sentences = []
    output_sentences = []

    #retrieve the keywords
    for line in keyword_file:
        line = line.lower().replace('\n', '').replace('\r', '')
        if len(line) < 2:
            break
        keywords[line]= True

    #read sentences in input
    cnt_line = 0
    for line in input_file:
        cnt_line += 1

        if mode == "review":
            if cnt_line == part_id * num_new_quest + 1:
                shuffle(input_sentences)
                input_sentences = input_sentences[:(num_new_quest + num_old_quest)]
                break
        else:  #the defaut mode is "new"
            #push old and new sentences to input_sentences
            if cnt_line == (part_id - 1) * num_new_quest + 1:
                shuffle(input_sentences)
                input_sentences = input_sentences[:num_old_quest]
            if cnt_line == part_id * num_new_quest + 1:
                break

        #preprocessing lines
        line = line.lower().replace('\n', '').replace('\r', '')
        input_sentences.append(line)

        # count number studied words so far
        for w in stop_words:
            line = line.replace(w, '')
        words = line.split(' ')
        for word in words:
            words_canvas[word] = True



    for line in input_sentences:
        words = line.split(' ')
        keyLine = []
        for word in words:
            if word in keywords:
                keyLine.append(word)
        if len(keyLine) == 0:
            continue
        shuffle(keyLine)

        #pick the first word in keyLine as the keyword
        for id in range (len(words)):
            if words[id] == keyLine[0]:
                words[id] = '__________'
                output = ' '.join(words) + '\n'
                output = keyLine[0] + '|' + output
                output_sentences.append(output)
                break

    #write output to file
    for output in output_sentences:
        output_file.write(output)
        print (output[:-1])


    #print number of words so far
    print("\n------------------------\n")
    print ("Number of words so far:", len(words_canvas))

if __name__ == '__main__':
    class_name = sys.argv[1]
    part_id = int(sys.argv[2])
    mode = sys.argv[3]
    generate_quizlet(class_name, part_id, mode)


# python generate_quizlet.py sunny 15 review
