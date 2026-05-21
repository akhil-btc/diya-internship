tokens:
its how an LLM processess things. it takes data by chunks, instead of words or senetences. these chunks CAN be words, parts of the word, spaces, more than one word, etcetera. LLMs process tokens in english charecters, so using other language alphabets like chinese, hindi, and french take more tokens for individual charecters. 

hallucinations:
when the model gives false information. if asked a fake questions, like what is the square root of negative 9 and the model gives three, that is a hallucination. while the data may have some sort of truth to it, the answer itself is still false, and when an LL gives this informaion, it is called a hallucination. it is "hallucinating" an answer and givin it to you.

context window
the amount of text that the LLM can see. it's like theh memory for an LLM. whatever is in the current context window can be pulled back at any point in the conversation. if the context window does not incude the previous conversation details, it cannot give the answers from before. it's like a security camera, which doesnt hold footage for its entire recording, only about 30 days. you can always go back to any tim ein those thirty days, but not past it. you can go to day 26 footage, but not day 39.

next-token predictions:
when the llm predicts what comes next. it looks  at the previous chunks of data and then at possible answers for that. it chooses based on the probablity of it being right and gives the next token. its like autocorrect. it learns from previous users and data, and based off of tht, it predicts the next tokens.


