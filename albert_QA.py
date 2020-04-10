import os
import torch
import time
from fuzzywuzzy import fuzz
# Needs Fuzzy Wuzzy
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
'''
pip install ./transformers
pip install tensorboardX
pip install fuzzywuzzy
Edit config_file to your local Albert Question Answering or everything will not work
Also download your own Albert Model here
https://s3.amazonaws.com/models.huggingface.co/bert/ktrapeznikov/albert-xlarge-v2-squad-v2/pytorch_model.bin
'''

from transformers import AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer, squad_convert_examples_to_features
# import (
#     AlbertConfig,
#     AlbertForQuestionAnswering,
#     AlbertTokenizer,
#     squad_convert_examples_to_features
# )

from transformers.data.processors.squad import SquadResult, SquadV2Processor, SquadExample

from transformers.data.metrics.squad_metrics import compute_predictions_logits

# READER NOTE: Set this flag to use own model, or use pretrained model in the Hugging Face repository

use_own_model = False

if use_own_model:
    model_name_or_path = "/content/model_output"
else:
    model_name_or_path = "ktrapeznikov/albert-xlarge-v2-squad-v2"
# Edit this to your local path ***OR nothing will work***
config_file = "./Albert Question Answering"

output_dir = ""

# Config
n_best_size = 1
max_answer_length = 30
do_lower_case = True
null_score_diff_threshold = 0.0

    # Setup model
config_class, model_class, tokenizer_class = (
    AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer)
# config = config_class.from_pretrained(model_name_or_path)
config = config_class.from_pretrained(config_file)
# tokenizer = tokenizer_class.from_pretrained(
#     model_name_or_path, do_lower_case=True)
tokenizer = tokenizer_class.from_pretrained(
    config_file, do_lower_case=True)
# model = model_class.from_pretrained(model_name_or_path, config=config)
model = model_class.from_pretrained(config_file, config=config)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)

processor = SquadV2Processor()

class SnippetAnswer:

    def __init__(self,  snippet, answer):
        self.snippet = snippet
        self.answer = answer


def to_list(tensor):
    return tensor.detach().cpu().tolist()

def run_prediction(question_texts, context_text):
    """Setup function to compute predictions"""
    examples = []

    for i, question_text in enumerate(question_texts):
        example = SquadExample(
            qas_id=str(i),
            question_text=question_text,
            context_text=context_text,
            answer_text=None,
            start_position_character=None,
            title="Predict",
            is_impossible=False,
            answers=None,
        )

        examples.append(example)

    features, dataset = squad_convert_examples_to_features(
        examples=examples,
        tokenizer=tokenizer,
        max_seq_length=384,
        doc_stride=128,
        max_query_length=64,
        is_training=False,
        return_dataset="pt",
        threads=1,
    )

    eval_sampler = SequentialSampler(dataset)
    eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=10)

    all_results = []

    for batch in eval_dataloader:
        model.eval()
        batch = tuple(t.to(device) for t in batch)

        with torch.no_grad():
            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "token_type_ids": batch[2],
            }

            example_indices = batch[3]

            outputs = model(**inputs)

            for i, example_index in enumerate(example_indices):
                eval_feature = features[example_index.item()]
                unique_id = int(eval_feature.unique_id)

                output = [to_list(output[i]) for output in outputs]

                start_logits, end_logits = output
                result = SquadResult(unique_id, start_logits, end_logits)
                all_results.append(result)

    output_prediction_file = "predictions.json"
    output_nbest_file = "nbest_predictions.json"
    output_null_log_odds_file = "null_predictions.json"

    predictions = compute_predictions_logits(
        examples,
        features,
        all_results,
        n_best_size,
        max_answer_length,
        do_lower_case,
        output_prediction_file,
        output_nbest_file,
        output_null_log_odds_file,
        False,  # verbose_logging
        True,  # version_2_with_negative
        null_score_diff_threshold,
        tokenizer,
    )

    return predictions


def question_answering_albert(relevant_snippets, question, threshold=70):
    answers = []
    answer_map = {}
    max_sim = 0
    final_answer = ''
    final_snippet = ''
    # Finds answers for each snippet
    for snippet in relevant_snippets:
        predictions = run_prediction(question, snippet)
        for key in predictions.keys():
            snippetAnsObj = SnippetAnswer(snippet, predictions[key])
            answers.append(snippetAnsObj)

    # Returns the answer if it appears in snippets frequently. Returns the longest
    # answer in case of ties. If there is no answer it will return an empty string

    for answer in answers:
        if answer.answer not in answer_map.keys():
            answer_map[answer.answer] = [1, answer.snippet]
        else:
            answer_map[answer.answer] = [answer_map[answer.answer][0] + 1, answer.snippet]
        for key in answer_map:
            if fuzz.ratio(key.lower(), answer.answer.lower()) > threshold:
                answer_map[key] = [answer_map[key][0] + 1, answer.snippet]
                answer_map[answer.answer] = [answer_map[key][0] + 1, answer.snippet]
    for key in answer_map.keys():
        if max_sim < answer_map[key][0]:
            # print("Inside if")
            # print(key)
            # print(answer_map[key][1])
            final_answer = key
            max_sim = answer_map[key][0]
            final_snippet = answer_map[key][1]
        elif max_sim == answer_map[key][0]:
            if len(final_answer) < len(key):
                # print("Inside elif")
                final_answer = key
                final_snippet = answer_map[key][1]

    if final_answer == '':
        final_snippet = ''

    print(final_answer)
    print(final_snippet)
    return final_answer, final_snippet


# This has to be called by this type of main because run prediction uses threading
'''
if __name__ == '__main__':
    question_answering_albert(["The capital of Washington is Olympia"], ["What is the capital of Washington"])
'''