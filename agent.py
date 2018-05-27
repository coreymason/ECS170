from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
import tensorflow as tf
import numpy as np



####################################################################################
"""A random agent for starcraft."""

"""remove later, this is for environment testing purposes only"""

class RandomAgent(base_agent.BaseAgent):
  """A random agent for starcraft."""

  def step(self, obs):
    super(RandomAgent, self).step(obs)
    function_id = numpy.random.choice(obs.observation.available_actions)
    args = [[numpy.random.randint(0, size) for size in arg.sizes]
            for arg in self.action_spec.functions[function_id].args]
    return actions.FunctionCall(function_id, args)
##################################################################################


class A2CAgent:
    def __init__(self, sess, policy, discount=.99, learning_rate=1e-4, max_gradient_norm=1):
        print('A2C init')
        self.sess = sess
        self.policy = policy
        self.discount = discount #TODO: use discount from sc2_env observation instead, won't need this class var then
        self.learning_rate = learning_rate
        self.max_gradient_norm = max_gradient_norm

    def _build(self):
        self.action, self.value = self.policy.build()
        #loss =

        optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate, decay=0.99, epsilon=1e-5)
        self.train_op = tf.layers.optimize_loss(
            loss=loss,
            global_step=tf.train.get_global_step(),
            optimizer=optimizer,
            clip_gradients=self.max_gradient_norm,
            learning_rate=None,
            name="train_op")

    def act(self, observation):
        # Use observation
        return self.sess.run([self.action, self.value])

    def train(self, observations, actions, rewards, dones, values, next_value):
        returns = self.get_returns(rewards, dones, values, next_value)
        advantages = returns - values
        print('A2C train')

    # Compute return values as return = reward + discount * next value * (0 if done else 1)
    def get_returns(self, rewards, dones, values, next_value):
        returns = np.zeros((rewards.shape[0], rewards.shape[1]), dtype=np.float32)
        # Compute last one individually with next_value
        returns[-1] = rewards[-1] + self.discount * next_value * (1 - dones[-1])
        # Compute rest in a loop with values
        for i in reversed(range(returns.size[0] - 1)):
            returns[i] = rewards[i] + self.discount * values[i+1] * (1 - dones[i])
        return returns
