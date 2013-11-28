import random

# This function is use to generate random code with length limitation
def codeGenerator(num_chars):
  code_set = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  code = ''
  return ''.join(random.choice(code_set) for x in range(num_chars))

