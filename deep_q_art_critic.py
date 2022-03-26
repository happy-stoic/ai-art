import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts


class ArtCriticEnvironment(py_environment.PyEnvironment):
    """Make an Art Critic environment for TensorFlow."""

    def __init__(self):
        # We have 2 actions; 0 user doesn't like it, 1 user does like it.
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=1, name='action')
        # The observation is whether we like the painting or not.
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=0, name='observation')
        self._state = 0
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = 0
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.int32))

    def _step(self, action):

        if self._episode_ended:
        # The last action ended the episode. Ignore the current action and start
        # a new episode.
            return self.reset()

        # If user has added input.
        # TODO: add input here; you like it or you don't
        if action == 1:
            self._episode_ended = True
        elif action == 0:
        # TODO: user rates it out of ten, that's what the state becomes.
            new_card = np.random.randint(1, 11)
            self._state += new_card
        else:
            raise ValueError('`action` should be 0 or 1.')

        if self._episode_ended or self._state >= 21:
            #TODO: make the reward equal the value entered by the user.
            reward = self._state - 21 if self._state <= 21 else -21
            return ts.termination(np.array([self._state], dtype=np.int32), reward)
        else:
            return ts.transition(
                np.array([self._state], dtype=np.int32), reward=0.0, discount=1.0)