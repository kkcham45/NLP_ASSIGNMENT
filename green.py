import conceptnet_lite
from conceptnet_lite import Label, edges_for
from nrclex import NRCLex
from better_profanity import profanity
import openai
import random

conceptnet_lite.connect("")

def get_emotion_words(word, emotion):
    # list of words to return
    emotion_words = []
    no_emotions = []

    # list of relations to search
    relations = ['related_to','form_of','is_a','part_of','used_for','capable_of','causes','has_subevent','has_first_subevent','has_prerequisite','has_property','synonym','antonym','distinct_from','derived_from','defined_as','has_context','similar_to','etymologically_related_to','receives_action']

    # check for profanity in word
    if profanity.contains_profanity(word) == True:
        print('Sorry, there is no information for this word')
        return []

    # get associated words
    usecases = []
    for i in relations:
        for e in edges_for(Label.get(text = word, language ='en').concepts, same_language = True):
            if(e.relation.name == i and e.start.text == word):
                if e.end.text not in usecases and profanity.contains_profanity(e.end.text) == False:
                    usecases.append(e.end.text.replace('_',' '))

        for e in edges_for(Label.get(text = word, language ='en').concepts, same_language = True):
            if(e.relation.name == i and e.end.text == word):
                if e.start.text not in usecases and profanity.contains_profanity(e.start.text) == False:
                    usecases.append(e.start.text.replace('_',' '))

    # check emotion of each word
    for word in usecases:
        emo_dict = NRCLex(word).affect_frequencies

        # add word to emotion_words list if it has the specified emotion
        if emotion in emo_dict.keys() and emo_dict[emotion] > 0:
            emotion_words.append(word)
        else:
            no_emotions.append(word) 
    
    if len(emotion_words) == 0:
        return no_emotions
    else:
        return emotion_words



# def generate_story(prompt, character, emotion):
#     # set up API client
#     openai.api_key = "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"
def generate_story(prompt, character, emotion):
    # Replace this with your own logic to generate stories based on the prompt, character, and emotion
    story_template = f"This is a story about {character} experiencing {emotion} while dealing with {prompt}."
    return story_template


    # generate story
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"#prompt : pen #idea : A student is in an examination hall. He starts imagining his family members pressurising him to get good marks. Once he opens his pencil box and hold the pen, he feels confident and writes the exam really well. This depicts how a good pen that offers comfort while writing can ease the students pressures while writing an exam. #prompt : Air Conditioning #idea : A couple has a discussion on buying an Air conditioning. Wife buys the Air Conditioning without discussing with him. Husband advices her that she could have done some research before buying one. Then wife explains all the features the Air Conditioning provides which makes it best in the market. #prompt : Chocolate #idea : A small girl enters a grocery store with her mother. The mother looks tensed and worried while speaking to someone on the phone. The girl goes to the shop keeper and asks for a chocolate. She gives her toys one by one as money. The shop keeper gives her the chocolate and in return gives a small toy as change. The girl gives the chocolate to her mother and wishes Happy Birthday!. This makes the mother feel happy and hugs her daughter. #prompt : Bulb #idea : Husband and wife talk to each other in the video call. Husband is on an office trip. He gets a call from his boss and asks his wife to stay on line. While he is speaking to his boss he notices that his wife fell asleep. So he switches the lights off in his house with the help his mobile phone. This shows how smart bulbs are helpful. #prompt: Television #idea: A family of four is gathered around their television in the living room. They are watching a movie and eating popcorn. The youngest member of the family is so absorbed in the show that he hardly notices his siblings passing him popcorn and making funny comments about the actors. This shows how television brings an entire family together for some quality time. #prompt: Flower Vase #idea: A woman is having a tough day at work and is feeling low. She decides to take a break and goes to the nearby florist. She buys a beautiful flower vase and brings it home. She looks at the vase and smiles. She arranges the flowers in the vase to create a stunning bouquet. Looking at the vase and the flowers, she feels relaxed and happier. This illustrates how flowers in a vase can bring joy and peace to someone's day.#prompt: Photo frame #idea: A family is gathered together to celebrate the grandmother's 80th birthday. As a surprise, the family presents her with a photo frame. As grandmother looks at the frame, she starts reminiscing about the times spent with her family. This shows how a photo frame can evoke fond memories and bring joy to the elderly. #prompt: Suitcase as a bomb #idea: A young girl is travelling alone on a bus. She notices an unattended suitcase in the corner of the bus and gets suspicious. She immediately alerts the authorities who check the suitcase and find it to be a bomb. This illustrates how even the most innocuous objects can be used as a weapon of terror. #prompt: Travelling in a flight #idea: A family is travelling to another city in a flight. They are all excited to reach the destination and explore the new city. The family is looking out of the window and the little ones are asking questions about the birds and the clouds. This shows how travelling in a flight can be fun and exciting for the entire family.#prompt: Cool drink in Christmas celebration #idea: It is Christmas celebration and a family is gathered around the Christmas tree. They open their presents and enjoy the delicious Christmas feast. The little ones ask for a cool drink and the father brings out a can of soda from the refrigerator. The family cheers and enjoy the festive season with a cool drink in hand. This illustrates how a simple thing like a cool drink can add joy to a special occasion. #prompt: Generate a story advertising {prompt} with an emotion of {emotion} with charateristics of {character}",
        temperature=0.7,
        max_tokens=370,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # get generated text
    story = response["choices"][0]["text"]

    # return first 200 words of story
    return story

def get_story(word, emotion):
    stories = []
    words = get_emotion_words(word, emotion)
    if len(words) > 10:
        ten_words = random.sample(words, 10)
        for i in ten_words:
            stories.append(generate_story(word, emotion, i))
    else:
        for i in words:
            stories.append(generate_story(word, emotion, i))
    # if len(emotion_words) == 0:
    #     if len(no_emotion_words) > 10:
    #         #If there are no emotion words and no emotion words have a number greater than 10
    #         ten_no_emotion_words = random.sample(no_emotion_words, 10)
    #         for i in ten_no_emotion_words:
    #             stories.append(generate_story(word, emotion, i))
    #     else :
    #         #If there are no emotion words and no emotion words have a number less than 10
    #         for i in no_emotion_words:
    #             stories.append(generate_story(word, emotion, i))
    # else:
    #     if len(emotion_words) > 10:
    #         #If there are emotion words and emotion words have a number greater than 10
    #         ten_emotion_words = random.sample(emotion_words, 10)
    #         for i in ten_emotion_words:
    #             stories.append(generate_story(word, emotion, i))
    #     else:
    #         #If there are emotion words and emotion words have a number less than 10
    #         for i in emotion_words:
    #             stories.append(generate_story(word, emotion, i))

    return stories



if __name__ == '__main__':
    word = input("Enter a word: ")
    emotion = input("Enter an emotion: ")
    
    output_story = get_story(word, emotion)
    output_words = get_emotion_words(word, emotion)
    
    print("Output Story:")
    for story in output_story:
        print(story)

    print("\nOutput Words:")
    print(output_words)