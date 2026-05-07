import numpy
import numpy as np


def dot (vec_a,vec_b):
    if(len(vec_a) != len(vec_b)):
        raise ValueError("2个向量维度必须一致")
    dot_sum = 0
    for a,b in zip(vec_a,vec_b):
        dot_sum += a * b

    return dot_sum

def get_norm(vec):
    norm = 0
    for i in vec:
        norm += i ** 2
    return np.sqrt(norm)

def cos_sim(vec_a,vec_b):
    result = dot(vec_a,vec_b) / (get_norm(vec_a) * get_norm(vec_b))
    return  result

if __name__ == '__main__':
    vec_a = [0.5,0.5]
    vec_b = [0.7,0.7]
    vec_c = [0.7, 0.5]
    vec_d = [-0.7, 0.7]

    print("vec_a和vec_b的余弦相似度:",(cos_sim(vec_a,vec_b)))
    print("vec_a和vec_c的余弦相似度:",(cos_sim(vec_a,vec_c)))
    print("vec_a和vec_d的余弦相似度:",(cos_sim(vec_a,vec_d)))
