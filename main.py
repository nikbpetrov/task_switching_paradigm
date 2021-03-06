"""
Hit play to execute the task switching paradigm!!!
__________________________________________

"""
import taskSwitching as tS
from psychopy import visual
from pyniexp import scannersynch
import enum

 
# Set some useful constants
class Config(enum.Enum):
    SYNCH_CONFIG = 'config.json'
    IN_SCANNER = False
    TR = 2                          # seconds
    MIN_LOG_LEVEL = 'INFO'
    QUIT_BUTTON = 'q'


if __name__ == '__main__':

    # Query participant details
    gui = tS.ParticipantGUI()
    participant = gui.participant

    # Create the window we'll display the experiment in
    win = visual.Window(
        size=[1000, 1000],
        units="pix",
        fullscr=False,
        color=[0, 0, 0],
        winType='pyglet',
        gammaErrorPolicy="warn"
    )

    text = visual.TextStim(
        text="Scanner synch... preparing",
        win=win,
        font='monospace',
        color=[1, 1, 1]
    )
    text.draw()
    text.win.flip()

    # Create interface for scanner pulse and response box
    SSO = scannersynch.scanner_synch(
        config=Config.SYNCH_CONFIG.value,
        emul_synch=not Config.IN_SCANNER.value,
        emul_buttons=not Config.IN_SCANNER.value
    )
    SSO.set_synch_readout_time(0.5)
    SSO.TR = Config.TR.value

    SSO.set_buttonbox_readout_time(0.5)
    if not SSO.emul_buttons:
        SSO.add_buttonbox('Nata')
    else:
        SSO.buttons = ['1', '2', '3']
    SSO.control_buttons = [Config.QUIT_BUTTON.value]

    text.text = "Scanner synch... starting"
    text.draw()
    text.win.flip()

    SSO.start_process()

    # Run tutorial #
    # Create the experiment object
    tut = tS.ExperimentTaskSwitch(
        window=win,
        panel_size=[800, 800],
        synch=SSO,
        config=Config,
        participant=participant,
        feedback_duration=2,
        run_sequence=[],
        trials=[None],
        save_enabled=False
    )
    tut.trials = [
        tS.ComponentInfoCard(
            experiment=tut,
            next_task=tut.TrialTypes.DIGIT_SPAN.value,
            break_duration=tut.InfoCardDurations.LONG.value
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.DIGIT_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.DIGIT_SPAN, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.DIGIT_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.DIGIT_SPAN, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.DIGIT_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.DIGIT_SPAN, experiment=tut)
        ),
        tS.ComponentInfoCard(
            experiment=tut,
            next_task=tut.TrialTypes.SPATIAL_SPAN.value,
            break_duration=tut.InfoCardDurations.LONG.value
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_SPAN, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_SPAN, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_SPAN,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_SPAN, experiment=tut)
        ),
        tS.ComponentInfoCard(
            experiment=tut,
            next_task=tut.TrialTypes.SPATIAL_ROTATION.value,
            break_duration=tut.InfoCardDurations.LONG.value
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_ROTATION,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_ROTATION, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_ROTATION,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_ROTATION, experiment=tut)
        ),
        tut.create_trial_by_type(
            tut.TrialTypes.SPATIAL_ROTATION,
            experiment=tut,
            stimulus=tut.create_stimulus_by_type(tut.TrialTypes.SPATIAL_ROTATION, experiment=tut)
        ),
    ]

    # Run the experiment
    tut.synch.wait_for_synch()
    tut.run()

    # Run main experiment #
    # Create the experiment object
    exp = tS.ExperimentTaskSwitch(
        window=win,
        panel_size=[800, 800],
        synch=SSO,
        config=Config,
        participant=participant
    )

    # Debugging
    exp.debug_trial_order()
    exp.save_trial_order()

    
    # Run the experiment
    exp.synch.wait_for_synch()
    exp.run()
    
    exp = None
    win.close()
    SSO._scanner_synch__process.terminate()
    SSO = None
