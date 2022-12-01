import codecs
import os
import pathlib
import random
import re
import sys
import time
from psychopy import core, data, event, logging, visual
from pyglet.window import key

# from src.library import *
def parse_instructions(input_data: str) -> list:
    """
    parse instruction into pages
    page break is #
    """
    return re.findall(r"([^#]+)", input_data)


def load_instruction(PATH: str) -> list:
    """
    load and then parse instrucition
    return a list
    """
    PATH = (
        f"{os.path.dirname(os.path.abspath(__file__))}//resources//ESQ//ESQ_instr.txt"
    )
    with codecs.open(PATH, "r", encoding="utf8") as f:
        input_data = f.read()
    return parse_instructions(input_data)


class my_instructions(object):
    """
    show instruction and wait for trigger
    """

    def __init__(
        self,
        window,
        instruction_txt,
        ready_txt,
        instruction_size,
        instruction_font,
        instruction_color,
        parseflag,
    ):
        """
        Initialize the instruction object.
        Args:
            window: The window object.
            settings: The settings dictionary.
            instruction_txt: The instruction text.
            ready_txt: The ready text.
            instruction_size: The instruction size.
            instruction_font: The instruction font.
            instruction_color: The instruction color.
            parseflag: The parse flag.
        Returns:
            None
        """
        self.window: visual.Window = window
        self.instruction_txt: str = load_instruction(instruction_txt)
        self.ready_txt: str = load_instruction(ready_txt)[0]
        self.display: visual.TextStim = visual.TextStim(
            window,
            text="default text",
            font=instruction_font,
            name="instruction",
            color="black",
        )
        self.parseflag: bool = parseflag

    def showf(self: object, pathlib: object, event: object) -> None:
        """
        This function shows the instruction text.
        """
        lines = pathlib.Path("instructions/You_instr.txt").read_text()
        instext = lines
        self.display.setText(instext)
        self.display.draw()
        self.window.flip()
        event.waitKeys(keyList=["return"])


def runexp(
    filename: str,
    timer: object,
    win: object,
    writers: list,
    resdict: dict,
    runtime: int,
    dfile: str,
    seed: int,
    movietype: str = None,
) -> None:
    """
    This is a function that runs the experiment.
    """
    random.seed()
    rs = random.randint(0, 10000)
    random.seed(a=rs)
    writera = writers[0]
    writerb = writers[1]
    if movietype != None:
        resdict["Assoc Task"] = movietype
    instr_path = "./taskScripts/resources/ESQ/"  # path for instructions
    fixed_ESQ_name = f"{os.path.dirname(os.path.abspath(__file__))}//resources//ESQ//ESQ_Questions.csv"
    win.flip()
    instruction_parameter = dict(
        [
            ("inst_size", 34),  # size/height of the instruction
            ("inst_color", "black"),  # color of the instruction
            ("inst_font", "sans"),  # color of the instruction
        ]
    )
    ready_txt = f"{instr_path}wait_trigger.txt"
    # settings = get_settings(env="lab", ver="A")
    ESQ_txt = f"{instr_path}ESQ_instr.txt"
    ESQ_msg = my_instructions(
        window=win,
        instruction_txt=ESQ_txt,
        ready_txt=ready_txt,
        instruction_size=instruction_parameter["inst_size"],
        instruction_font=instruction_parameter["inst_font"],
        instruction_color="black",
        parseflag=0,
    )
    lines = pathlib.Path(
        f"{os.path.dirname(os.path.abspath(__file__))}//resources//ESQ//ESQ_instr.txt"
    ).read_text()
    ESQ_msg.display.setText(lines)
    ESQ_msg.display.draw()
    ESQ_msg.window.flip()
    event.waitKeys(keyList=["return"])
    # ESQ_msg.show()
    win.flip()
    ES_fixed = data.TrialHandler(
        nReps=1,
        method="sequential",
        trialList=data.importConditions(fixed_ESQ_name),
        name="Questionnaire",
    )
    ratingScale = visual.RatingScale(
        win,
        low=1,
        high=10,
        markerStart=4.5,
        precision=10,
        tickMarks=[1, 10],
        markerColor="black",
        textColor="black",
        lineColor="black",
        acceptPreText="Use the left and right arrow keys",
        acceptSize=3,
    )
    QuestionText = visual.TextStim(
        win, color="black", text=None, anchorHoriz="center", anchorVert="top"
    )
    scale_high = visual.TextStim(
        win, text=None, wrapWidth=None, color="black", pos=(0.5, -0.5)
    )
    scale_low = visual.TextStim(
        win, text=None, wrapWidth=None, color="black", pos=(-0.5, -0.5)
    )
    random.shuffle(ES_fixed.trialList)
    inc = 0.1
    #       get each question from Questionnaire:
    for i in range(len(ES_fixed.trialList)):
        event.clearEvents()
        if i < len(ES_fixed.trialList):
            question = ES_fixed.next()
            (
                resdict["Timepoint"],
                resdict["Time"],
                resdict["Experience Sampling Question"],
            ) = ("ESQ", timer.getTime(), str(question["Label"] + "_start"))
            writera.writerow(resdict)
            (
                resdict["Timepoint"],
                resdict["Time"],
                resdict["Experience Sampling Question"],
                resdict["Experience Sampling Response"],
                resdict["Auxillary Data"],
            ) = (None, None, None, None, None)
        ratingScale.noResponse = True
        rand = random.randrange(1, 10, 1)
        ratingScale.markerStart = rand
        keyState = key.KeyStateHandler()
        win.winHandle.push_handlers(keyState)
        pos = ratingScale.markerStart
        ratingScale.noResponse = True
        while ratingScale.noResponse:  # key 4 not pressed
            if keyState[key.LEFT] is True:
                pos -= inc
            elif keyState[key.RIGHT] is True:
                pos += inc
            if pos > 9:
                pos = 9
            elif pos < 0:
                pos = 0
            ratingScale.setMarkerPos(pos)
            QuestionText.setText(question["Questions"])
            QuestionText.draw()
            scale_high.setText(question["Scale_high"])
            scale_low.setText(question["Scale_low"])
            scale_high.draw()
            scale_low.draw()
            ratingScale.draw()
            win.flip()
        time.sleep(1)
        responded = ratingScale.getRating()
        (
            resdict["Timepoint"],
            resdict["Time"],
            resdict["Experience Sampling Question"],
            resdict["Experience Sampling Response"],
            resdict["Auxillary Data"],
        ) = (
            "ESQ",
            timer.getTime(),
            str(question["Label"] + "_response"),
            responded,
            str(f"Marker Started at {str(rand + 1)}"),
        )
        writera.writerow(resdict)
        writerb.writerow(resdict)
        (
            resdict["Timepoint"],
            resdict["Time"],
            resdict["Experience Sampling Question"],
            resdict["Experience Sampling Response"],
            resdict["Auxillary Data"],
        ) = (None, None, None, None, None)
