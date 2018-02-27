# LanguageModel
Learn a Language Model on corpus and generate a random sentence

Task1:

We are various Language Models with multiple advanced smoothing techniques like Kneser-Ney, Katz, Linear-Interpolation e.t.c

To run code just the the shell script ./LM.sh
1. It will first read the corpus and after preprocessing shuffle the sentences and split the data in devlopment and train.
2. There are four settings of Data Set (Look at the report for that)
3. Code will  count all the bigrams, trigrams and related stuff
4. It then tune the hyperparameters on the coressponding devlopment datasets in all of the four settings.
5. In end, it gives test results : which includes the perplexity on coressponding test dataset for all the models(i.e Linear Interpolation, Katz's Backoff, Kneser-Ney)

Task2:

After that you can run the script generate_sentence.sh
It will generate the random sentence.
