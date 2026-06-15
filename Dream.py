import os
import platform
import subprocess
import time
import json
from openai import OpenAI

#initiate model/download model if not exists and run with unique system-prompt, can be different styles for different audience

from pathlib import Path

def get_valid_path(path_str: str) -> Path:
    # 1. Create Path object (handles / vs \ automatically)
    p = Path(path_str)

    # 2. Normalize & convert to absolute path
    # strict=False works even if the file doesn't exist yet (Python 3.6+)
    resolved = p.resolve(strict=False)

    return resolved

model_path = str(get_valid_path("LLM/Qwen3-0.6B-Q8_0.gguf"))

base = str(get_valid_path("LLM"))

model_name="Qwen3-0.6B-Q8_0.gguf"

"""

if not Path(model_path).is_file():

    from huggingface_hub import hf_hub_download
    import joblib

    REPO_ID = "Qwen"
    FILENAME = "Qwen3-0.6B-GGUF"

    model = joblib.load(
        hf_hub_download(repo_id=REPO_ID, local_dir=base,filename=FILENAME)
    )

"""

port_num=8080

buffer=input("Input the port number for running server, leave alone for default:8080")

if buffer:
    port_num=buffer

buffer=str(input("Input the path for local model to be used, leave alone for bundled Qwen3-0.6B"))

if buffer:
    model_path=str(get_valid_path(buffer))
    alias="user-defined"
    buffer=str(input("Input the path for model to be used, leave alone for generic name \"user-defined\""))
    if buffer:
        alias=buffer
    else:
        alias="user-defined"

binary=str(get_valid_path("LLM/bin/llama-server"))

init_command = binary + ' -n -1 -cmoe -cram 32 --no-warmup -fa off --no-jinja --numa distribute --temp 0 --top_p 0.99 --top_k 32 --min_p 0.05 -m '

config=model_path +" --port "

config+=str(port_num)

init_command+=config

input("Paste the command into powershell or console and modify as you wish, press enter in the window after doing so:" + init_command)

base_path="http://127.0.0.1:"+str(port_num)

#new stuff

client = OpenAI(base_url=base_path,api_key='None')

"""

response = str(client.chat.completions.create(
    model=model_name,
    messages=[{"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals."}]
))

"""

replies={}
questions={}

# 1. Welcoming and How are you? emotions+feelings for state, habits and dreams, factual not how you feel you are but who you really are

def welcome():
    replies["feelings and emotions"]=str(input("Hi user, how are you? Could you tell me more about your journey of feelings/emotions from this week to currently? Please be honest to yourself!\n"))
    print("What you are doing these days determine who you are ten years later! Take part in who you are proud of, not in AI alone")
    replies["habits and dreams"]=str(input("Would you mind sharing more about your recent habits, regardless of how well you think about them, and your value/priorities and dreams? No matter small, large or almost unachievable, just brainstorm the best life you want to achieve!\n"))

    internal="Here is a journey of emotions and feelings that the user had from his past week up to the current moment.\n"
    internal+=replies["feelings and emotions"]

    internal="Here is a list of habits that the user has done from his past week up to the current moment.\n"
    internal+=replies["habits and dreams"]

    internal+="Generate three or more reflective questions that highlight any lack of strong correlation or causation in thoughts, incompleteness in the scope of thinking or inconsistency in logical thinking in relation to the previous conversations that might be unobvious to the user, so as to encourage the user to ponder."

    # generate from section one replies

    response = client.chat.completions.create(
        model=model_name,
        messages=[
        {"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals. Do NOT use Markdown, code blocks, or extra commentary."},
        {"role": "user", "content": internal}],
        response_format={"type": "text"},
        stream = False
    ).choices[0].message.content
    print(response)
    # process JSON into list of questions

    return questions(response) #prompting from AI questions

# 2. Analyze situation through follow-up questions

def questions(list_of_Q_A):
    #from AI generate questions to further discover
        prompt = "The user has a reply to the questions\n"
        prompt+=list_of_Q_A
        prompt+="\n"
        answer=str(input(list_of_Q_A))
        replies[list_of_Q_A]=answer
        prompt+=answer
        prompt+="\n"
        prompt+="Generate three or more reflective questions that highlight any lack of strong correlation or causation in thoughts, incompleteness in the scope of thinking or inconsistency in logical thinking in relation to the previous conversations that might be unobvious to the user, so as to encourage the user to ponder."
        response = client.chat.completions.create(
        model=model_name,
        messages = [{"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals. Do NOT use Markdown, code blocks, or extra commentary."},
        {"role": "user", "content": prompt}
                ],
        response_format={"type": "text"},
        stream = False
            ).choices[0].message.content
        print(response)
        new_thoughts=str(input("Anything to add or supplement?"))
        replies["Additional thoughts"]=new_thoughts

        return frameworks()

# 3. Give frameworks for user to fill-in themselves to match against situation analysis by AI

def frameworks():

    # generate markdown table framework from prev. replies, seperate tables of sections and contents
    framework=client.chat.completions.create(
        model=model_name,
        messages = [{"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals. Do NOT use Markdown, code blocks, or extra commentary."},
        {"role": "user", "content": "Based on previous conversations, generate a SWOT (Strengths, Weakness, Opportunities, Threats) analysis."}
    ],
    response_format={"type": "text"},
    stream = False
    ).choices[0].message.content# prompting

    print(framework)

    contents="Based on previous conversation and the following input in JSON format from user, compare and contrast the differences between your previous SWOT analysis and the user's opinion, and summarize by giving follow-up reflection questions.\n",

    response=client.chat.completions.create(
            model=model_name,
            messages = [{"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals. Do NOT use Markdown, code blocks, or extra commentary."},
        {"role": "user", "content": contents}
        ],
        response_format={"type": "text"},
        stream = False
    ).choices[0].message.content


    #genAI thinking/processing and review, give advice and follow-up critical thinking questions

    print(response)

    return set_up()

# 5. Make Promise and set attitude and altitude through plans and goals with advice and quotes, short term/ long term

def set_up():

    #genAI give planning direction and frameworks, user modify roster

    framework=client.chat.completions.create(
        model=model_name,
        messages= [
        {"role": "system", "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful. Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful. Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful. Explore all related concepts, patterns and rationale to achieve operational and functional understanding. Explain all possible agendas, approaches, definitions, styles, techniques, focus, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit. Show logical connections, differences and interplay using analogies, comparisons and roleplaying. Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions. Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests. Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities. The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals. Do NOT use Markdown, code blocks, or extra commentary."},
        {"role": "user", "content": "Based on previous conversations, generate a \"Situation, Plan, Action, Result\" analysis."}
    ],
    response_format={"type": "text"},
    stream = False
    ).choices[0].message.content
    print(framework)
    print("Change as it fits!")
    # compile JSON table file for user

    end_condition_met=str(input("Please input \"Yes\" if you are satisfied with the plan to end here or \"No\" if you want to start again"))

    if end_condition_met=="Yes":
        return
    else:
        welcome()

# 6. Repeat!
welcome()
