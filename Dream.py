"""

from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen3-0.6B-GGUF",
    filename="*Q8_0.gguf",
    verbose=False,
    temperature=0,
    top_p=0.98,
    top_k=64,
    min_p=0.05
    max_tokens=-1
    last_n_tokens_size=32
)

llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful.
Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful.
Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful.
Explore all related concepts, patterns and rationale to achieve operational and functional understanding.
Explain all possible agendas, definitions, styles, techniques, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit.
Show logical connections, differences and interplay using analogies, comparisons and roleplaying.
Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions.
Ask all possible open-ended what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests.
Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities.",

//refer to latest ver. on desktop
        }
    ]
)

"""
import os
import requests
import platform
import subprocess
import time
from openai import OpenAI

#initiate model/download model if not exists and run with unique system-prompt, different styles for different audience

from pathlib import Path

def get_valid_path(path_str: str) -> Path:
    # 1. Create Path object (handles / vs \ automatically)
    p = Path(path_str)

    # 2. Normalize & convert to absolute path
    # strict=False works even if the file doesn't exist yet (Python 3.6+)
    resolved = p.resolve(strict=False)

    return resolved

model_path = get_valid_path("./Qwen3-0.6B-Q8_0.gguf")


if not Path(model_path).is_file():

    from huggingface_hub import hf_hub_download
    import joblib

    REPO_ID = "Qwen"
    FILENAME = "Qwen3-0.6B-GGUF"

    model = joblib.load(
        hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
    )

port_num=8080

base="Qwen3-0.6B-Q8_0.gguf"

buffer=input("Input the port number for running server, leave alone for default:8080")

if buffer:
    port_num=buffer

buffer=input("Input the path for local model to be used, leave alone for bundled Qwen3-0.6B")

if buffer:
    model_path=get_valid_path(buffer)
    alias="user-defined"
    buffer=input("Input the path for model to be used, leave alone for generic name \"user-defined\"")
    if buffer:
        alias=buffer
    else:
        alias="user-defined"

init_command = "alias qwen-='~/LLM/bin/llama-server -n -1 -cmoe -cram 32 --jinja --no-warmup -fa off --numa distribute --temp 0 --top_p 0.99 --top_k 32 --min_p 0.05 -m "

alias=base+" --port"

alias+=port_num

alias+="'"

init_command+=alias

#old stuff


"""

os.environ['CONFIG_FILE'] = {
    "host": "0.0.0.0",
    "port": port_num,
    "model": model_path,
    "model_alias": alias,
    "offload_kqv": True,
    "flash_attn:": True,
    "temperature": 0,
    "top_p": 0.99,
    "top_k": 32,
    "min_p": 0.05,
    "max_tokens": -1,
    "last_n_tokens_size": 16,
    "verbose": False
}
"""


shell_cmd = "cmd" if platform.system() == "Windows" else "bash"
shell = subprocess.Popen(
    [shell_cmd],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    text=True
)

shell.stdin.write(init_command + "\n")
shell.stdin.flush()


#new stuff

client = OpenAI(base_url="http://localhost:8080/v1/chat/completions")



response = client.responses.create(
    model=base,
    instructions="Ensure there are no gaps or assumptions before answering by doubting with questions internally, and present all possible reasons in the order of impact only when helpful.
Reaffirm with logical induction and deduction based on facts only, with step-by-step, case-by-case, level-by-level intuition internally, and display intuition only when helpful.
Prioritize quality and effectiveness, brevity and clarity, using frameworks and tables when helpful.
Explore all related concepts, patterns and rationale to achieve operational and functional understanding.
Explain all possible agendas, definitions, styles, techniques, objectives, relevance, significance, considerations, principles, assumptions, evidence, patterns, implications, extensions, biases, edge cases, corner cases, outliers, uncertainty, limitations, flaws, follow-up options, and counter-arguments, explicit or implicit.
Show logical connections, differences and interplay using analogies, comparisons and roleplaying.
Evaluate adaptability and sustainability with applicable and relatable contexts and scope and alternatives by asking where, who, when reflection questions.
Ask all possible open-ended what, what-if, how and why reflection questions that challenge convention and beliefs and arouse curiosity, creativity and interests.
Use paradoxes, dilemmas or dichotomies to illustrate all possible conundrums or ambiguities.
The following is a review of the current situation. Make use of all the available information to comprehend and ultimately coming up with a clean, specific follow-up plan for the user to track its progress on achieving his/her goals.",
    store=true
)



replies={}
questions={}

# 1. Welcoming and How are you? emotions+feelings for state, habits and dreams, factual not how you feel you are but who you really are

def welcome():
    replies={}
    replies["feelings and emotions"]=input("Hi user, how are you? Could you tell me more about your journey of feelings/emotions from this week to currently? No one is to judge about them and please be honest to yourself!")
    print("What you are doing these days determine who you are ten years later! Take part in who you are proud of, not in AI alone")
    replies["habits and dreams"]=input("Would you mind sharing more about your recent habits, regardless of how well you think about them, and your value/priorities and dreams? No matter small, large or almost unachievable, just brainstorm the best life you want to achieve!")

    internal="Here is a journey of emotions and feelings that the user had from his past week up to the current moment.\n"
    internal+=replies["feelings and emotions"]

    internal="Here is a list of habits that the user has done from his past week up to the current moment.\n"
    internal+=replies["habits and dreams"]

    internal+="Generate three or more reflective questions that highlight any lack of strong correlation or causation in thoughts, incompleteness in the scope of thinking or inconsistency in logical thinking in relation to the previous conversations that might be unobvious to the user, so as to encourage the user to ponder. Return the questions only in JSON format, with keys \"index\"(int) starting at 1 and \"questions\"(string). If there are no further questions to ask, return \"NULL\" for the key \"questions\""

    # generate from section one replies

    response = client.responses.create(
        model=base,
        input=internal,
        store=false
    )
    # process JSON into list of questions

    return questions(json.loads(response)) #prompting from AI starting questions

# 2. Analyze situation through follow-up questions

def questions(list_of_Q_A):
    #from AI generate questions to further discover

    if list_of_Q_A:
        for item in list_of_Q_A:
            prompt = "The user has a reply to the question\n"
            question=item["questions"]
            if question:
                prompt+=question
                prompt+="\n"
                answer=input(question)
                replies[question]=answer
                prompt+=answer
                prompt+="\n"
                prompt+="Generate three or more reflective questions that highlight any lack of strong correlation or causation in thoughts, incompleteness in the scope of thinking or inconsistency in logical thinking in relation to the previous conversations that might be unobvious to the user, so as to encourage the user to ponder. Return the questions only in JSON format, with keys \"index\"(int) starting at 1 and \"questions\"(string). If there are no further questions to ask, return \"NULL\" for the key \"questions\""
                response = client.responses.create(
                model=base,
                input=prompt
                store=false
            )
            else:
                return questions(NULL)
        #from AI prompt follow-up questions
    response = client.responses.create(
        model=base,
        input="Generate three or more reflective questions that highlight any lack of strong correlation or causation in thoughts, incompleteness in the scope of thinking or inconsistency in logical thinking in relation to the previous conversations that might be unobvious to the user, so as to encourage the user to ponder. Return the questions only in JSON format, with keys \"index\"(int) starting at 1 and \"questions\"(string). If there are no further questions to ask, return \"NULL\" for the key \"questions\""
        store=false
    ) #prompt for new_follow-up questions
        return questions(response)

    else:
        new_thoughts=input("Anything to add or supplement?")
        replies["Additional thoughts"]=new_thoughts

        return frameworks()

# 3. Give frameworks for user to fill-in themselves to match against situation analysis by AI

def frameworks():

    # generate markdown framework from prev. replies, seperate tables of sections and content
    framework={} # prompting
    framework_response={}
    # ask users to fill in tables
    for table in framework:
        for section in table.keys():
            framework_reponse[section]=input(section)

    replies.update(framework_response)

    for ai, user in zip(framework,framework_response):
        #prompting for comparison
        print("AI vs You")

    new_thoughts=input("Anything to add or supplement?")
    replies["Additional thoughts"]+="\n"
    replies["Additional thoughts"]+="After using frameworks"
    replies["Additional thoughts"]+=new_thoughts

    return comparison()

# 4. Compare and contrast thought and reality

def comparison():

    #genAI thinking/processing and review, give advice and follow-up critical thinking questions
    suggestions="" #prompting
    print(suggestions)

    new_thoughts=input("Anything to add or supplement?")
    replies["Additional thoughts"]+="\n"
    replies["Additional thoughts"]+="After overall situation review"
    replies["Additional thoughts"]+=new_thoughts

    return set_up()

# 5. Make Promise and set attitude and altitude through plans and goals with advice and quotes, short term/ long term

def set_up():

    #genAI give planning direction and frameworks, user modify roster
    suggestions="" #prompting
    print(suggestions)

    print("Change as it fits!")
    # compile excel table file for user

    end_condition_met=input("Please input \"Yes\" if you are satisfied with the plan to end the program or \"No\" if you want to start again")

    if end_condition_met="Yes":
        shell.terminate()
        shell.wait()
        return
    else
        welcome()

# 6. Repeat!
welcome()