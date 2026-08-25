from tf_agents.environments import suite_gym

env = suite_gym.load('CartPole-v0')
print('Environment created:', env)
print(env.time_step_spec())
