from dqn.user_simulator import UserSimulator
from dqn.error_model_controller import ErrorModelController
from dqn.dqn_agent import DQNAgent
from dqn.state_tracker import StateTracker
import pickle, argparse, json
from dqn.user import User
from dqn.utils import remove_empty_slots
from response.agent_response import *
import pymongo
def get_agent_action(state_tracker,dqn_agent,user_action,done=False):
    state_tracker.update_state_user(user_action)
    current_state = state_tracker.get_state(done)
    _, agent_action = dqn_agent.get_action(current_state)
    state_tracker.update_state_agent(agent_action)
    return agent_action
